from curses import wrapper
import src.app as app
if __name__ == "__main__":
	wrapper(app.main)