## [Angular donut-chart](https://nervetattoo.github.io/angular-chart-donut)

A simple donut chart for Angular built on d3

* `bower install angular-chart-donut`
* `npm install angular-chart-donut`

```js
angular.module('mymodule', ['chart.donut']);
```
```html
<chart-donut data="modeldata" title="Percentage awesomeness" size="150"></chart-donut>
```

<img src="https://nervetattoo.github.io/angular-chart-donut/images/shot.png">

### Element attribute options

* `data`  Bind to an integer ranging from 0 to 100
* `title` Use this title for the drop-pin
* `color` Optionally set a color. This can also be achieved through CSS overrides
* `symbol` Defaults to `%` but can be set to other values, like empty string
* `size`  Pixel size of chart, if not set the chart will attempt to size itself by its parent, but if parent does not have a size while the chart is rendered this will fail.

### Contributors

* [Raymond Julin](http://twitter.com/nervetattoo)
* [Christian Leon Christensen](http://twitter.com/chrleon) — Design
