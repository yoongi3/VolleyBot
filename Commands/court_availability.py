from bs4 import BeautifulSoup
from discord.ext import commands
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


WEEKDAYS = {'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'}

def init_driver(headless=True):
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")  # Enable headless mode
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def navigate_and_search(driver, date):
    url = f"https://secure.activecarrot.com/public/facility/browse/487/1848/{date.strftime('%Y-%m-%d')}"

    driver.get(url)
    wait = WebDriverWait(driver, 10)
    iframe = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f"iframe[src*='/public/facility/iframe/487/1848/{date.strftime('%Y-%m-%d')}']")))
    driver.switch_to.frame(iframe)

@commands.command(name="next", help="Finds court availability starting [Y] weeks ahead for the next [X] days")
async def next(ctx, wks=1, num_days=8):
    start = datetime.now().date() + timedelta(weeks=wks)
    await scrape(ctx, start, num_days)

@commands.command(name="courts", help="Court availability for the next [X] days.")
async def courts(ctx, num_days=8):
    start = datetime.now().date()    
    await scrape(ctx, start, num_days)

async def scrape(ctx, start, num_days):
    driver = init_driver()

    if driver is None:
        print("Driver is not initialized.")
        return
    
    for day in range(num_days):
        date_to_scrape = start + timedelta(days=day)
        navigate_and_search(driver, date_to_scrape)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        court_list = soup.select("[id*=booking_calendar]")
        days_away = (date_to_scrape - datetime.now().date()).days 
        link = f"https://secure.activecarrot.com/public/facility/browse/487/1848/{date_to_scrape.strftime('%Y-%m-%d')}"
        await ctx.send(f"**[{date_to_scrape} {date_to_scrape.strftime('%A')}]({link}) ({days_away} days away)**")

        court_num=1
        for court in court_list:
            time_blocks = court.find_all(class_='fc-event')

            if len(time_blocks) == 1:
                continue   

            block_data = extract_block_data(time_blocks)
            booked_times = get_times(block_data)
            available_times = get_available(booked_times)

            # Weeknights only
            if date_to_scrape.strftime('%A') in WEEKDAYS:
                desirable_times = filter_desirables(available_times)

                if desirable_times is None:
                    continue

                formatted_times = format_times(desirable_times)
                await ctx.send(f"court {court_num}: {formatted_times}")

                court_num+=1
                continue

            formatted_times = format_times(available_times)
            await ctx.send(f"court {court_num}: {formatted_times}")

            court_num+=1
        await ctx.send("\u200b")
    driver.close()
    return
    
def format_times(times):
    # Join the times with commas and spaces to format them in a single line
    formatted_times = " | ".join(times)
    return formatted_times

def extract_block_data(time_blocks):
    block_data = []
    for block in time_blocks:
        style_dict = dict(item.strip().split(': ') for item in block.get('style').split(';') if item.strip())
        top_value = int(style_dict.get('top', '0')[:-2])
        height_value = int(style_dict.get('height', '0')[:-2])
        block_data.append({"top": top_value, "height": height_value})

    block_data.sort(key=lambda x: x['top'])

    return block_data

def filter_desirables(available_times):
    desirables = []
    for times in available_times:
        start_time_str, end_time_str = times.split(' - ')
        end_time = datetime.strptime(end_time_str, '%I:%M%p')
        
        if end_time.hour >= 19: # filters out courts that cant be booked past 19:00
            desirables.append(times)
    
    return None if not desirables else desirables

def decimal_to_HHMM(decimal_time):
    hours = int(decimal_time)
    minutes = int((decimal_time - hours) * 60)

    # Convert 24-hour format to 12-hour format
    period = 'AM' if hours < 12 else 'PM'
    hours = hours % 12
    if hours == 0:
        hours = 12 

    return f"{hours}:{minutes:02}{period}"


def get_times(blocks):
    booked_times = []
    for index, block in enumerate(blocks):
        if index == 0:  # Handle first block
            start = 5
            end = ((block['height'] + 2) / 42 + 5) 
        elif index == len(blocks) - 1:  # Handle last block
            start = (block['top'] + 1) / 42 + 5
            end = 23
        else:  # Handle all other blocks
            start = (block['top'] + 1) / 42 + 5
            end = (block['height'] + 2) / 42 + start

        formatted_start = decimal_to_HHMM(start)
        formatted_end = decimal_to_HHMM(end)

        booked_times.append({'start': formatted_start, 'end': formatted_end})

    return booked_times
        
def get_available(blocks):
    available_times = []
    for i in range(len(blocks)-1):
        if blocks[i+1]:
            start = blocks[i]['end']
            end = blocks[i+1]['start']
        available_times.append(f"{start} - {end}")
    return(available_times)