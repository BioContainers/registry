ngDonut
=======

![Travis](http://img.shields.io/travis/Wildhoney/ngDonut.svg?style=flat)
&nbsp;
![npm](http://img.shields.io/npm/v/ng-donut.svg?style=flat)
&nbsp;
![License MIT](http://img.shields.io/badge/License-MIT-lightgrey.svg?style=flat)

* **Heroku**: [http://ng-donut.herokuapp.com/](http://ng-donut.herokuapp.com/)
* **Bower:** `bower install ng-donut`

`ngDonut` is a tiny Angular and D3 component which renders a donut graph &ndash; which is capable of animation when the values change!

<img width="300" height="300" src="http://i.imgur.com/9LVVbJC.png" />

---

# Getting Started

All that you need to do to begin is add the `donut` node to the DOM and attach your dataset using the `ng-model` attribute:

```html
<donut ng-model="myDataset"></donut>
```

`myDataset` should be defined as an array of values:

```javascript
$scope.myDataset = [100, 200, 300, 400, 500];
```

`ngDonut` currently supports the following styling attributes: `width`, `height`, `radius`, `stroke`, `stroke-width`  and `colours`.

## Colours

You should define your `colours` attribute as an array of possible colours &ndash; otherwise `ngDonut` will utilise D3's [ordinal colours](https://github.com/mbostock/d3/wiki/Ordinal-Scales).

# Advanced Models

Often you'll wish to pass more complex models to `ngDonut` which will allow you to create a relationship between the visualised data and the raw data &ndash; in these cases you'll want to pass your entire models, which may look something similar to the following:

```javascript
$scope.myDataset = [
    { name: 'Adam', age: 29 },
    { name: 'Maria', age: 23 },
    { name: 'Gabriele', age: 33 }
];
```

You can simply pass the aforementioned array into the `donut` node using the `ng-model` attribute &ndash; however you'll also need to provide the `property` attribute to notify `ngDonut` which property to use for the values:

```html
<donut ng-model="myDataset" property="'age'"></donut>
```

With this the donut will be created as normal, but `ngDonut` will be using your full models which is especially useful for events.

# Mouse Events

When a user mouses over an arc in the donut &ndash; or when they move their mouse out &mdash; or even click on an arc &mdash; then it is nice to respond to that with perhaps a tooltip. Thankfully `ngDonut` supports the following mouse events:

 * `mousemove`;
 * `mouseleave`;
 * `click`;

As an example we'll use the `mousemove` mouse event which you'll need to configure on the `donut` node:

```html
<donut ng-model="myDataset" property="'age'" mousemove="mouseMoved(model)"></donut>
```

From there you can safely configure your scope method which will be invoked:

```javascript
// Excuse the ES6 syntax...
$scope.mouseMoved = model => $log.info(model);
```

Please take a look at the tooltip [example in `Application.js`](https://github.com/Wildhoney/ngDonut/blob/master/example/js/Application.js) for how to create a tooltip using the `mousemove` and `mouseleave` events.