import utility
import time

def main():
    browser = utility.login("USER", "PASS")
    threads = utility.threads("threads")
    for thread in threads:
        message = utility.get_porn(thread[0])
        utility.post(message, thread[1], browser)
        time.sleep(60)

if __name__ == '__main__':
    main()
