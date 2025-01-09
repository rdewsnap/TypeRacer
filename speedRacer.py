from pynput.keyboard import Key, Listener, Controller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

# Initialize the keyboard controller
keyboard = Controller()

# URL of the page to be automated
URL = "https://play.typeracer.com/"  # Replace with your target URL

# CSS Selector for the <span> elements to read
SPAN_SELECTOR = 'span[unselectable="on"]'

# Function to read text from the <span> elements on the page
def read_span_text(driver):
    try:
        span_elements = driver.find_elements(By.CSS_SELECTOR, SPAN_SELECTOR)
        span_texts = []
        for i, span in enumerate(span_elements):
            if span.get_attribute("unselectable") == "on":
                text = span.text
                if i == 0:
                    text = text.rstrip()  # Remove trailing spaces from the first span
                elif i == 1:
                    text = text.lstrip()  # Remove leading spaces from the second span
                span_texts.append(text)
            else:
                break
        # Concatenate the texts and remove the first space if necessary
        result_text = " ".join(span_texts)
        if len(result_text) > 1 and result_text[1] == ' ':
            result_text = result_text[0] + result_text[2:]
        return result_text
    except NoSuchElementException:
        print("Span elements not found.")
        return None
    except Exception as e:
        print(f"Error finding spans: {e}")
        return None

# Function to simulate typing the text as keystrokes
def execute_as_keystrokes(text):
    if text:
        # Type the first character separately
        first_char = text[0]
        keyboard.press(first_char)
        keyboard.release(first_char)
        time.sleep(0.1)  # Add a slight delay for realism

        # Type the rest of the characters
        for char in text[1:]:
            keyboard.press(char)
            keyboard.release(char)
            time.sleep(0.05)  # Add a slight delay between keystrokes for realism

# Main function to set up the browser and handle keyboard events
def main():
    print("Initializing browser...")
    # Set up the browser
    driver = webdriver.Chrome()  # Or use webdriver.Firefox(), etc.
    driver.get(URL)
    time.sleep(3)  # Wait for the page to load

    span_text = None

    # Function to handle key press events
    def on_press(key):
        nonlocal span_text
        try:
            if key.char == "9":  # Press '9' to read the span text
                print("Reading text from the spans...")
                span_text = read_span_text(driver)
                if span_text:
                    print(f"Read text: {span_text}")
                else:
                    print("No text found in the spans.")
            elif span_text and key.char == span_text[0]:  # Type the first character manually
                print("Executing span text as keystrokes...")
                execute_as_keystrokes(span_text[1:])  # Pass the rest of the text to the function
        except AttributeError:
            # Handle special keys (non-character keys)
            pass

    # Listener for keyboard events
    try:
        print("Starting listener...")
        with Listener(on_press=on_press) as listener:
            listener.join()
    except Exception as e:
        print(f"Listener error: {e}")

    # Clean up
    driver.quit()

if __name__ == "__main__":
    main()