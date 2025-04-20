import multiprocessing
from webapp import run_app_process
from worker import run_worker_process

def main():
    # Create separate processes for worker and app
    worker_process = multiprocessing.Process(target=run_worker_process)
    app_process = multiprocessing.Process(target=run_app_process)

    # Start both processes
    worker_process.start()
    app_process.start()

    # Wait for both processes to complete
    try:
        worker_process.join()
        app_process.join()
    except:
        print("Main process interrupted. Terminating child processes...")
        worker_process.terminate()
        app_process.terminate()
        worker_process.join()
        app_process.join()

if __name__ == "__main__":
    main()