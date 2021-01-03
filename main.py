from FundMonitor import fundMonitor
from apscheduler.schedulers.blocking import BlockingScheduler

if __name__ == '__main__':
    a = """
      ______               _   __  __             _ _             
     |  ____|             | | |  \/  |           (_) |            
     | |__ _   _ _ __   __| | | \  / | ___  _ __  _| |_ ___  _ __ 
     |  __| | | | '_ \ / _` | | |\/| |/ _ \| '_ \| | __/ _ \| '__|
     | |  | |_| | | | | (_| | | |  | | (_) | | | | | || (_) | |   
     |_|   \__,_|_| |_|\__,_| |_|  |_|\___/|_| |_|_|\__\___/|_|   
                                                              
    """
    print(a)

    fundMonitor()
    scheduler = BlockingScheduler()
    scheduler.add_job(fundMonitor, 'cron', day_of_week='0-4', hour=22, minute=00)
    scheduler.start()

