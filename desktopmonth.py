import utility


def main():
    browser = utility.login("USER", "PASS")
    month = utility.get_month_text()
    year = utility.get_year()
    title = "Escritorios de {} de {}".format(month, year)
    message = "Ya sabéis de qué va el tema. Si vais a poner una sola imagen, ponedla directamente :D"
    utility.new_thread(message, title, 13, 6, browser)

if __name__ == '__main__':
    main()
