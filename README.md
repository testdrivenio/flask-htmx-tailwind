# Rapid Prototyping with Flask, htmx, and Tailwind CSS

### Want to learn how to build this?

Check out the [post](https://testdriven.io/blog/flask-htmx-tailwind/).

## Want to use this project?

1. Fork/Clone

1. Create and activate a virtual environment:

    ```sh
    $ python3 -m venv venv && source venv/bin/activate
    ```

1. Install the Python dependencies:

    ```sh
    (venv)$ pip install -r requirements.txt
    ```

1. Configure Tailwind CSS:

    ```sh
    (venv)$ tailwindcss
    ```

1. Scan the templates and generate CSS file:

    ```sh
    (venv)$ tailwindcss -i ./static/src/main.css -o ./static/dist/main.css --minify
    ```

1. Run the app:

    ```sh
    (venv)$ python app.py
    ```

1. Test at [http://localhost:5000/](http://localhost:5000/)
