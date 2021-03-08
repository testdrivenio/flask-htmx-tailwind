# Rapid Prototyping with Flask, htmx, and Tailwind CSS

In this tutorial, you'll learn how to set up Flask with [htmx](https://htmx.org/) and [Tailwind CSS](https://tailwindcss.com/). The goal of both htmx and Tailwind is to simplify modern web development so you can design and enable interactivity without ever leaving the comfort and ease of HTML. We'll also look at how to use [Flask-Assets](https://flask-assets.readthedocs.io/) to bundle and minify static assets in a Flask app.

## htmx

[htmx](https://htmx.org/) is a library that allows you to access modern browser features like AJAX, CSS Transitions, WebSockets, and Server-Sent Events directly from HTML, rather than using JavaScript. It allows you to build user interfaces quickly with hypertext.

htmx extends several features already built into the browser, like making HTTP requests and responding to events. For example, rather than only being able to make GET and POST requests via `a` and `form` elements, you can use HTML attributes to send GET, POST, PUT, PATCH, or DELETE requests on any HTML element:

```html
<button hx-delete="/user/1">Delete</button>
```

You can also update parts of a page to create a Single-page Application (SPA):

```
<p class="codepen" data-height="265" data-theme-id="light" data-default-tab="html,result" data-user="mjhea0" data-slug-hash="RwoJYyx" style="height: 265px; box-sizing: border-box; display: flex; align-items: center; justify-content: center; border: 2px solid; margin: 1em 0; padding: 1em;" data-pen-title="RwoJYyx">
  <span>See the Pen <a href="https://codepen.io/mjhea0/pen/RwoJYyx">
  RwoJYyx</a> by Michael Herman (<a href="https://codepen.io/mjhea0">@mjhea0</a>)
  on <a href="https://codepen.io">CodePen</a>.</span>
</p>
<script async src="https://cpwebassets.codepen.io/assets/embed/ei.js"></script>
```

Watch the `network tab`. When the button is clicked, an XHR request is sent to the `https://v2.jokeapi.dev/joke/Any?format=txt&safe-mode` endpoint. The request's response is then appended to the `p` with an `id` of `output.

> For more examples, check out the [UI Examples](https://htmx.org/examples/) page from the official htmx docs.

### Pros and Cons

**Pros**:

1. TODO
1. TODO

**Cons**:

- Library Maturity. Since the library is quite new, documentation and example implementations are not enough for reference.
- Size of data transferred. Typically, SPA frameworks (like React and Vue) work by passing data back and forth between the client and server in JSON format. The data received is then rendered by the client. htmx, on the other hand, receives the rendered HTML from the server, and it replaces the target element with the response. The HTML in rendered format is typically larger in terms of size than a JSON response.

## Tailwind CSS

[Tailwind CSS](https://tailwindcss.com/) is a "utility-first" CSS framework. Rather than shipping pre-build components (like [Bootstrap](https://getbootstrap.com/) or [Bulma](https://bulma.io/)), it provides many building blocks (utility classes) that enable one to create layouts and designs easily and quickly.

For example, take the following HTML and CSS:

```html
<style>
.hello {
  height: 5px;
  width: 10px;
  background: gray;
  border-width: 1px;
  border-radius: 3px;
  padding: 5px;
}
</style>

<div class="hello">Hello World</div>
```

This can be implemented with Tailwind like so:

```html
<div class="h-1 w-2 bg-gray-600 border rounded-sm p-1">Hello World</div>
```

Check out the [CSS Tailwind Converter](https://tailwind-converter.netlify.app/) to convert CSS to Tailwind. Compare the results.

### Pros and Cons

**Pros**:

- Highly customizable. Although Tailwind comes with pre-built classes, they can be overwritten using the *tailwind.config.js* file.
- Optimization. PurgeCSS can remove all the unused CSS classes from the Tailwind CSS file, reducing the size of the CSS bundle.
- Dark mode. It's effortless to implement dark mode: `<div class="bg-white dark:bg-black">`

**Pros**:

- Tailwind does not provide any official prebuilt components like buttons, cards, nav bars, an so forth. Components have to be created from scratch. There are a few community-driven resources for components like [Tailwind CSS Components](https://tailwindcomponents.com/) and [Tailwind Toolbox](https://www.tailwindtoolbox.com/), to name a few.
- CSS is inline. This couples content and design, which increases the page size and clutters the HTML.

## Flask-Assets

[Flask-Assets](https://flask-assets.readthedocs.io/) is an extension designed for managing static assets in a Flask application. With it, you create a simple asset pipeline for:

1. Compiling [Sass](https://sass-lang.com/) and [LESS](http://lesscss.org/) to CSS stylesheets
1. Combining and minifying multiple CSS and JavaScript files down to a single file for each
1. Creating asset bundles for use in your templates

With that, let's look at how to work with each of the above projects in Flask!

## Project Setup

To start, create a new directory for our project, create and activate a new virtual environment, and install Flask along with Flask-Assets:

```bash
$ mkdir flask-htmx-tailwind && cd flask-htmx-tailwind
$ python3.9 -m venv venv
$ source .venv/bin/activate
(venv)$

(venv)$ pip install Flask==1.1.2 Flask-Assets==2.0
```

Next, let's install Tailwind CSS, [PostCSS]([PostCSS](https://github.com/postcss/postcss)), [Autoprefixer](https://github.com/postcss/autoprefixer), and [PurgeCSS](https://purgecss.com/) with [NPM](https://www.npmjs.com/):

```bash
$ npm install tailwindcss postcss postcss-cli autoprefixer @fullhuman/postcss-purgecss
```

Additional tools:

- PostCSS - a tool used by Tailwind for preprocessing CSS
- Autoprefixer - a PostCSS plugin that automatically transforms CSS to support different browsers
- PurgeCSS - removes unused CSS

Next, add an *app.py* file:

```python
# app.py

from flask import Flask
from flask_assets import Bundle, Environment

app = Flask(__name__)

assets = Environment(app)
css = Bundle("src/main.css", output="dist/main.css", filters="postcss")

assets.register("css", css)
css.build()
```

After importing [Bundle](https://flask-assets.readthedocs.io/en/latest/#flask_assets.Bundle) and [Environment](https://flask-assets.readthedocs.io/en/latest/#flask_assets.Environment), we created a new `Environment` and registered our CSS assets to it via a `Bundle`.

The `Bundle` that we created takes in *src/main.css* as an input, which will then be processed via PostCSS and outputted to *dist/main.css*. Behind the scenes, PostCSS runs like so using a Python subprocess:

```bash
$ postcss src/main.css -o dist/main.css
```

> Since all Flask static files reside in the "static" folder by default, the above-mentioned "src" and "dist" folders reside in the "static" folder.

With that, let's set up Tailwind and PostCSS.

Start by creating a Tailwind config file:

```bash
$ npx tailwind init
```

This should generate a *tailwind.config.js* file. All Tailwind customizations go into this file.

Next, add a *postcss.config.js* file:

```javascript
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
  ],
});
```

Add the following to the *static/src/main.css*:

```css
/* static/src/main.css */

@tailwind base;
@tailwind components;
@tailwind utilities;
```

Here, we defined all the `base`, `components`, and `utilities` classes from Tailwind CSS. PostCSS will build all the classes into the target location, *dist/main.css*.

Run the app:

```bash
(venv)$ python app.py
```

You should see a new directory named "dist" inside the "static" folder.

> If you get a `Program file not found: postcss`, try installing PostCSS globally: `npm install --global postcss postcss-cli`.

Take note of the generated *static/dist/main.css* file.

Now that you've seen how to set up Flask-Assets, let's look at how to serve up an *index.html* file to see the CSS in action.

## Simple Example

Update the *app.py* file like so:

```python
# app.py

from flask import Flask, render_template
from flask_assets import Bundle, Environment

app = Flask(__name__)

assets = Environment(app)
css = Bundle("src/main.css", output="dist/main.css", filters="postcss")

assets.register("css", css)
css.build()


@app.route("/")
def homepage():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
```

Create a "templates" folder. Then, add a *base.html* file to it:

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

    <title>Flask + htmlx + Tailwind CSS</title>
  </head>
  <body class="bg-blue-100">
    {% block content %}
    {% endblock content %}
  </body>
</html>
```

Take note of the `{% assets 'css' %` block. Since we registered the CSS Bundle with the app environment, we can access it using the registered name, `css`, and the `{{ ASSET_URL }}` will automatically use the path.

Also, we added some color to the HTML body via `<body class="bg-blue-100">`. `bg-blue-100` is used to change the [background color](https://tailwindcss.com/docs/background-color) to light blue.

Add the *index.html* file:


```html
<!-- templates/index.html -->

{% extends "base.html" %}

{% block content %}
<h1>Hello World</h1>
{% endblock content %}
```

Start the server via `python app.py` and navigate to [http://localhost:5000](http://localhost:5000) in your browser to see the results

With Tailwind configured, let's add htmx into the mix and build a live search that displays results as you type.

## Live Search Example

Rather than fetching the htmx library from a CDN, let's download it and use Flask-Assets to bundle it.

Download the library from [https://unpkg.com/htmx.org@1.2.1/dist/htmx.js](https://unpkg.com/htmx.org@1.2.1/dist/htmx.js) and save it to "static/src".

Now, to create a new bundle for our JavaScript files, update *app.py* like so:

```python
# app.py

from flask import Flask, render_template, request
from flask_assets import Bundle, Environment

from todo import todos


app = Flask(__name__)

assets = Environment(app)
css = Bundle("src/main.css", output="dist/main.css", filters="postcss")
js = Bundle("src/*.js", output="dist/main.js") # new

assets.register("css", css)
assets.register("js", js) # new
css.build()
js.build() # new


@app.route("/")
def homepage():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search_todo():
    search_term = request.form.get("search")

    if not len(search_term):
        return render_template("todo.html", todos=[])

    res_todos = []
    for todo in todos:
        if search_term in todo["title"]:
            res_todos.append(todo)

    return render_template("todo.html", todos=res_todos)


if __name__ == "__main__":
    app.run(debug=True)
```

Here, we created a new bundle named for our JavaScript files, which outputs to *static/dist/main.js*. Since we're not using any filters here, the source and target files will be the same.

Now we add the new asset to our *base.html* file:

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

    <!-- new -->
    {% assets 'js' %}
      <script type="text/javascript" src="{{ ASSET_URL }}"></script>
    {% endassets %}

    <title>Flask + htmlx + Tailwind CSS</title>
  </head>
  <body class="bg-blue-100">
    {% block content %}
    {% endblock content %}
  </body>
</html>
```

Navigate to [https://jsonplaceholder.typicode.com/todos](https://jsonplaceholder.typicode.com/todos) and save all the TODOs to a new file called *todo.py*.

We'll add the ability to search based on the title of each todo.

Add the following to the `index.html` file.

```html
<!-- templates/index.html -->
{% extends 'base.html' %}

{% block content %}
<div class="w-small w-2/3 mx-auto py-10 text-gray-600">
  <input
    type="text"
    name="search"
    hx-post="/search"
    hx-trigger="keyup changed delay:250ms"
    hx-indicator=".htmx-indicator"
    hx-target="#todo-results"
    placeholder="Search"
    class="bg-white h-10 px-5 pr-10 rounded-full text-2xl focus:outline-none"
  >
  <span class="htmx-indicator">Searching...</span>
</div>

<table class="border-collapse w-small w-2/3 mx-auto">
  <thead>
    <tr>
      <th class="p-3 font-bold uppercase bg-gray-200 text-gray-600 border border-gray-300 hidden lg:table-cell">#</th>
      <th class="p-3 font-bold uppercase bg-gray-200 text-gray-600 border border-gray-300 hidden lg:table-cell">Title</th>
      <th class="p-3 font-bold uppercase bg-gray-200 text-gray-600 border border-gray-300 hidden lg:table-cell">Completed</th>
    </tr>
  </thead>
  <tbody id="todo-results">
    {% include 'todo.html' %}
  </tbody>
</table>
{% endblock content %}
```

Let's take a moment to look at the attributes defined from htmx:

```html
<input
  type="text"
  name="search"
  hx-post="/search"
  hx-trigger="keyup changed delay:250ms"
  hx-indicator=".htmx-indicator"
  hx-target="#todo-results"
  placeholder="Search"
  class="bg-white h-10 px-5 pr-10 rounded-full text-2xl focus:outline-none"
>
```

1. The input sends a POST request to the `/search` endpoint.
1. The request is triggered via the keyup event with a delay of 250ms. So if a new keyup event is entered before 250ms elapses between the last keyup, the request is not triggered.
1. The HTML response from the request is then displayed in the `#todo-results` element.
1. We also have an indicator, a loading element that appears after the request is sent and disappears after the response comes back.

Add the *templates/todo.html* file:

```html
<!-- templates/todo.html -->

{% if todos|length>0 %}
  {% for todo in todos %}
    <tr class="bg-white lg:hover:bg-gray-100 flex lg:table-row flex-row lg:flex-row flex-wrap lg:flex-no-wrap mb-10 lg:mb-0">
      <td class="w-full lg:w-auto p-3 text-gray-800 text-center border border-b block lg:table-cell relative lg:static">{{todo.id}}</td>
      <td class="w-full lg:w-auto p-3 text-gray-800 text-center border border-b block lg:table-cell relative lg:static">{{todo.title}}</td>
      <td class="w-full lg:w-auto p-3 text-gray-800 text-center border border-b block lg:table-cell relative lg:static">
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

This file renders the TODOs that match our search query. Finally, add the route handler to *app.py*:

```python
@app.route("/search", methods=["POST"])
def search_todo():
    search_term = request.form.get("search")

    if not len(search_term):
        return render_template("todo.html", todos=[])

    res_todos = []
    for todo in todos:
        if search_term in todo["title"]:
            res_todos.append(todo)

    return render_template("todo.html", todos=res_todos)
```

The `/search` endpoint searches for the TODOs and renders the *todo.html* template with all the results.

Update the imports at the top:

```python
from flask import Flask, render_template, request
from flask_assets import Bundle, Environment

from todo import todos
```

Run the application using `python app.py` and navigate to [http://localhost:5000](http://localhost:5000) again to test it out

![final-demo](images/demo.gif)

EDITED TO HERE

## Removing unwanted CSS

The size of the *static/dist/main.css* is roughly 3.9MB because we generated the whole Tailwind CSS file. That said, since we are only using a few classes for styling, we can remove unused CSS via [PurgeCSS](https://purgecss.com/).

We already configured it earlier in *postcss.config.js*:

```javascript
process.env.FLASK_PROD === 'production' && require('@fullhuman/postcss-purgecss')({
  content: [
    path.resolve(__dirname, 'templates/**/*.html')
  ],
  defaultExtractor: content => content.match(/[A-Za-z0-9-_:/]+/g) || []
})
```

So, when `FLASK_PROD` is 'production', PurgeCSS wil walk through all the HTML files in the templates directory and remove unused CSS.

To test, fist set the environment variable:

```bash
(venv)$ export FLASK_PROD=production # for Linux

(venv)$ set FLASK_PROD=production # for windows
```

The, remove the dist and the cache folders, before starting the app:

```bash
(venv)$ rm -rf static/.webassets-cache static/dist
(venv)$ python app.py
```

Inspect the newly created *static/dist/main.css* file. It should now only be 12KB! Nice. Ensure the app still works before moving on.

## Conclusion

In this tutorial, we looked at how to:

- Set up Flask-Assets and Tailwind CSS
- Build a live search app using Flask, TailwindCSS, and htmx
- Remove unused CSS with PurgeCSS

htmx can render elements without reloading the page. Although this reduces the amount of work done on the client-side, the data sent from the sever can be higher since it's sending rendered HTML. The library is still young, but the future looks bright for it.

TODO: might be worth mentioning that websockets + html is starting to look trendy https://alistapart.com/article/the-future-of-web-software-is-html-over-websockets/

Tailwind is a powerful CSS framework that focuses on developer productivity. It's highly customizable.

TODO: can you add some resources for customizing

When using Flask, be sure to couple both htmx and Tailwind with Flask-Assets to simplify static asset management.

**Looking for some challenges?**

1. Minify the CSS and JavaScript output files via [cssmin](https://webassets.readthedocs.io/en/latest/builtin_filters.html#cssmin) and [jsmin](https://webassets.readthedocs.io/en/latest/builtin_filters.html#jsmin), respectively
1. Create different assets bundles for different environments and blueprints
1. Review the [included filters](https://webassets.readthedocs.io/en/latest/builtin_filters.html) that can be used with Flask-Assets
