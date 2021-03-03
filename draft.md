# Rapid Prototyping with Flask, HTMX, and Tailwind CSS

In this tutorial, we will learn how to set up Flask, [TailwindCSS](https://tailwindcss.com/) and [HTMX](https://htmx.org/) to build web applications. We'll use Flask for our backend, TailwindCSS for styling our frontend, and HTMX to render the HTML in parts. 

## What is HTMX?

> htmx allows you to access AJAX, CSS Transitions, WebSockets, and Server-Sent Events directly in HTML, using attributes so that you can build modern user interfaces with the simplicity and power of hypertext - Official documentation

Basically. htmx allows you to perform ajax, CSS transitions, etc., without writing any javascript code. HTMX makes the following possible,

- Any element can make HTTP requests.
- Event triggers other than `click` and `submit`
- All HTTP methods are available(GET, POST, PUT, PATCH, DELETE).
- Replace parts of the document, like a div or any other element, with the output, not the entire screen. 
- Follow the original web model, i.e., receive HTML response.

Let's see a quick example of how this works!!

```html
<script src="https://unpkg.com/htmx.org@1.2.1"></script>
<button hx-get="https://v2.jokeapi.dev/joke/Any?format=txt" hx-target="#output">
    Click Me
</button>

<div id="output"></div>
```

Paste the above code to an HTML file and run(or use the `quick-example.html` from the repository)

On top, we import the htmx library from CDN. Then we have two elements,

- A button with two attributes, `hx-get` and `hx-target`
- A div with id `output`

The code translates to,

*When the button is clicked, send a GET request to the URL and replace the `#output` element with the response*

![quick-example-demo](images/quick-example.gif)

Watch the `network tab`. When the button is clicked, an XHR(XMLHttpRequest) is sent to the endpoint. 


### Drawbacks of this model

A couple of drawbacks with this model are,

- The library is very young
- Documentation and example implementation is not enough for reference
- Size of data transferred

    Think of a todo app implementation in JS and HTMX. We can post the data for the javascript implementation and add a todo to the client-side based on the response status code. When the response is sent, we can have a custom status code(StatusCreated: 201, for example). 

    But in the case of HTMX, we render the todos and sent them back to the client. This can take up some bytes but think of the server's load for a high traffic application. 

## Tailwind CSS and Flask-Assets

> Rapidly build modern websites without ever leaving your HTML.

__Tailwind__ is a modern CSS framework that doesn't ship pre-built components. It treats CSS properties as HTML classes to style an element by simply adding/changing the class.

The highly customizable nature of tailwind makes it a trendy CSS framework.

__Flask-Assets__ helps you to integrate web assets into your Flask application. It takes in a single/multiple CSS/JS files and combines them into a single file and also supports plugins like [cssmin](https://github.com/zacharyvoase/cssmin) and [jsmin](https://github.com/tikitu/jsmin) to minify these files. 


## Setup Flask-Assets

Create a virtual environment and install the necessary python packages

```bash
# setup virtual environment
virtualenv .venv
source .venv/bin/activate

# install flask and flask-assets
pip install Flask==1.1.2 Flask-Assets==2.0
```

Next, let's install Tailwind, PostCSS, Autoprefixer, and PurgeCSS.

```bash
npm install tailwindcss postcss-cli autoprefixer @fullhuman/postcss-purgecss
```

- Tailwind - Our CSS framwork
- [PostCSS](https://github.com/postcss/postcss) - A tool for transforming styles with JS plugins
- [Autoprefixer](https://github.com/postcss/autoprefixer) - A PostCSS plugin that automatically transform CSS to support different browsers
- [PurgeCSS](https://purgecss.com/) - Remove unused CSS


Now let's setup flask-assets for tailwind CSS. Add the following to _app.py_

```python
# app.py

from flask import Flask
from flask_assets import Bundle, Environment

app = Flask(__name__)

css = Bundle("src/main.css", output="dist/main.css", filters="postcss")
assets = Environment(app)
assets.register("css", css)
css.build()
```

On the top, we imported the `Bundle` and `Environment` from Flask-Assets. Then we created a Bundle with input as `src/main.css` and output as `dist/main.css` with postcss filter. This actually runs the following command using python subprocess,

```bash
postcss src/main.css -o dist/main.css
```

PostCSS takes in the `src/main.css` and builds the CSS file to `dist/main.css`.

Then we created a new Environment. This registers the specified bundle into the Flask environment to build and include them later using Jinja syntax. 

Finally, the `css.build()` will execute the postcss build command. 

Add the following to the `static/src/main.css`.

> Since all Flask static files reside in `static` by default, the above-mentioned `src/main.css` and `dist/main.css` are in the static folder. 


```css
/* static/src/main.css */

@tailwind base;
@tailwind components;
@tailwind utilities;
```

We are defining all the `base`, `components`, and `utilities` classes of tailwind CSS. PostCSS will build all the classes into the target location.

Run the program using `python main.py`. You should see a new directory named `dist` inside the static folder. Inspect the `static/dist/main.css` file.

> In case you get an error saying `postcss not found`, install postcss globally using `npm i -g postcss-cli`

Now that you have seen how to setup flask assets let's serve our `index.html` and see the CSS in action. 

Complete the `main.py` by adding the following,

```python
# main.py

from flask import Flask
from flask_assets import Bundle, Environment

app = Flask(__name__)

css = Bundle("src/main.css", output="dist/main.css", filters="postcss")
assets = Environment(app)
assets.register("css", css)
css.build()


@app.route("/")
def homepage():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
```

Add the base template and include the assets that we built.

```html
<!-- templates/base.html -->

<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        
        {% assets 'css' %}
        <link rel="stylesheet" href="{{ ASSET_URL }}">
        {% endassets %}

        <title>Flask + HTMX + TailwindCSS</title>
    </head>
    <body class="bg-blue-100">
        {% block content %}
        {% endblock content %}
    </body>
</html>
```

Notice the `{% assets 'css' %` block in the above file. Since we registered the CSS Bundle with the app environment, we can access it using the registered name(`css`), and the `{{ ASSET_URL }}` will automatically use the path.

Also we added some color to the body using `<body class="bg-blue-100">`. The `bg-blue-100` is our tailwind style to change the background color to the lightest blue shade.


```html
<!-- templates/index.html -->

{% block content %}
<h1>Hello World</h1>
{% endblock content %}
```

Start the server using `python main.py` and navigate to http://localhost:5000 to see the result. Also, check out the `static/dist/main.css` to see the complete CSS built. _You should see a `Hello World` with blue body background_. 


## Live Search using Flask, HTML and TailwindCSS

Now that we have seen how to set up Flask and TailwindCSS, lets's build a live search that displays results as we type.

Include the htmx cdn to the head section of our base template.

```html
...
{% endassets %}
        
<script src="https://unpkg.com/htmx.org@1.2.1"></script>
<title>Flask + HTMX + TailwindCSS</title>
...
```

Navigate to https://jsonplaceholder.typicode.com/todos and save all the todos to a new file, `todo.py`.

```python
todos = [
  {
    "userId": 1,
    "id": 1,
    "title": "delectus aut autem",
    "completed": false
  },
  {
    "userId": 1,
    "id": 2,
    ...
```

We will search based on the title of each todo using the logic,

Add the following to the `index.html` file 

```html
<!-- templates/index.html -->
{% extends 'base.html' %}

{% block content %}
<div class="w-small w-2/3 mx-auto py-10 text-gray-600">

    <input type="text" name="search" hx-post="/search" hx-trigger="keyup changed delay:250ms"
        hx-indicator=".htmx-indicator" hx-target="#todo-results" placeholder="Search"
        class="bg-white h-10 px-5 pr-10 rounded-full text-2xl focus:outline-none">
    <span class="htmx-indicator">
        Searching...
    </span>
</div>
<table class="border-collapse w-small w-2/3 mx-auto">
    <thead>
        <tr>
            <th class="p-3 font-bold uppercase bg-gray-200 text-gray-600 border border-gray-300 hidden lg:table-cell">
                #</th>
            <th class="p-3 font-bold uppercase bg-gray-200 text-gray-600 border border-gray-300 hidden lg:table-cell">
                Title</th>
            <th class="p-3 font-bold uppercase bg-gray-200 text-gray-600 border border-gray-300 hidden lg:table-cell">
                Completed</th>
        </tr>
    </thead>
    <tbody id="todo-results">
        {% include 'todo.html' %}
    </tbody>
</table>
{% endblock content %}
```

Let's discuss the htmx defined here,

```html
<input type="text" name="search" hx-post="/search" hx-trigger="keyup changed delay:250ms"
        hx-indicator=".htmx-indicator" hx-target="#todo-results" placeholder="Search"
        class="bg-white h-10 px-5 pr-10 rounded-full text-2xl focus:outline-none">
```

The input will send a POST request to the `/search` endpoint. The request is triggered _on input with a delay of 250ms, so if a new character is entered within the 250ms, the request is not triggered_. The HTML response from the request is displayed in the `#todo-results` element, and also, we have an indicator, which is a loading element that pops up during the request until the response. 

You can see the `.htmx-indicator` just below the input element. 

```html
<!-- templates/todo.html -->

{% if todos|length>0 %}
{% for todo in todos %}
<tr
    class="bg-white lg:hover:bg-gray-100 flex lg:table-row flex-row lg:flex-row flex-wrap lg:flex-no-wrap mb-10 lg:mb-0">
    <td
        class="w-full lg:w-auto p-3 text-gray-800 text-center border border-b block lg:table-cell relative lg:static">
        {{todo.id}}
    </td>
    <td
        class="w-full lg:w-auto p-3 text-gray-800 text-center border border-b block lg:table-cell relative lg:static">
        {{todo.title}}
    </td>
    <td
        class="w-full lg:w-auto p-3 text-gray-800 text-center border border-b block lg:table-cell relative lg:static">
        {% if todo.completed %}
        <span class="rounded bg-green-400 py-1 px-3 text-xs font-bold">Yes</span>
        {% else %}
        <span class="rounded bg-red-400 py-1 px-3 text-xs font-bold">No</span>
        {% endif %}

    </td>
</tr>
{% endfor %}
{% endif %}
```

This file renders the todos that match our search description. Finally, update our app to include the search endpoint.

```python
# main.py

...
@app.route("/")
def homepage():
    return render_template("index.html", todos=[])


@app.route("/search", methods=["POST"])
def search_todo():
    search_term = request.form.get("search")
    if len(search_term) == 0:
        return render_template("todo.html", todos=[])
    res_todos = []
    for todo in todos:
        if search_term in todo["title"]:
            res_todos.append(todo)
    return render_template("todo.html", todos=res_todos)
...
```

The `/search` endpoint will search for the todos and render the `todo.html` with all the results. You should now understand why we wrote the todos in a separate HTML file.

Run the application using `python main.py` and navigate to http://localhost:5000 to test it out.

## Demo

![final-demo](images/demo.gif)

## Finishing up - Removing unwanted CSS

The size of our `static/dist/main.css` is roughly 3.8MB. This is because we generated the whole tailwind CSS file. The whole file is not required as we only used some of the classes for styling. To remove unused CSS, we will use the `purgecss` installed earlier.

Start by creating a tailwind config file.

```bash
npx tailwind init
```

This should generate a `tailwind.config.js` file. All the customizations for tailwind go into this file, but we leave it for now. 

Create a `postcss.config.js` and add the following to it. 

```js
const path = require('path');

module.exports = (ctx) => ({
    plugins: [
        require('tailwindcss')(path.resolve(__dirname, 'tailwind.config.js')),
        require('autoprefixer'),
        process.env.FLASK_PROD === 'production' && require('@fullhuman/postcss-purgecss')({
            content: [
                path.resolve(__dirname, 'templates/**/*.html')
            ],
            defaultExtractor: content => content.match(/[A-Za-z0-9-_:/]+/g) || []
        })
    ]
})
```

It looks for an environment variable named `FLASK_PROD`. If its value is "production", the purgecss will walk through all the HTML files in the templates directory. The final `static/dist/main.css` will only contain the CSS that we use in HTML files.

Let's see how this works.

```bash
# set the environment variable
export FLASK_PROD=production # for Linux

set FLASK_PROD=production # for windows
```

Remove the dist and the cache folder before starting the app.

```bash
rm -rf static/.webassets-cache
rm -rf static/dist
```

Now start the app, `python main.py`, and inspect the newly created `static/dist/main.css` file. __It's 12KB__. We have successfully removed unused CSS, and the app works the same as before.

## Conclusion

In this tutorial, we have seen,

- What is HTMX?
- Setting up Flask-Assets and TailwindCSS
- Building a live search app using Flask, TailwindCSS, and HTMX
- Remove unused CSS using purgeCSS

HTMX can render elements without reloading the page. Although this reduces the amount of work done on the client-side, the server amount(data) can be higher than the js-based frameworks. The library is very young, but maybe one-day, htmx can use it for building the frontend. Tailwind is a great CSS framework that offers customizability(we haven't seen much here). The framework does offer a CDN, which consumes ~71.5kB when compressed, which is 6x what we needed to build for this tutorial. Flask-Assets is a powerful tool for bundling static assets. 

### Looking for challenges?

- We haven't minified out the 12KB output CSS file. Try minifying it using `cssmin`. (Tip: `filters="postcss,cssmin"`)