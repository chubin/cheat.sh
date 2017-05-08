##Contributing

**Prerequisites**

Install [Node.js](https://nodejs.org/) and [npm](https://www.npmjs.com/). On OSX with [Homebrew](http://brew.sh/) installed it is as easy as:
```
brew install node
```

Install dependencies:
```
npm install
```

**Running tests**

Run tests once and exit:
```
npm test
```

Continuous mode. Whenever any source or test file changes, tests will run automatically:
```
karma start
```

Chrome starts automatically and stops on ```Ctrl+C```. You can also open ```http://localhost:9876/``` in any other browser and it will run the tests as long as the tab is open.

**Adding a test**

[Jasmine](http://jasmine.github.io/) is the testing framework used by Awesomplete.

To write a test (or suite of tests) start by adding a `describe` function which receives a string describing what is being tested and a function containing what you expect the test to do. Inside the function use the `it` block to arrange and assert a functionality.

A test would look like this:

```javascript
describe("A fact", function(){
    it("is always true",function(){
        var fact = true;
        expect(fact).toBe(true);
    });
});
```

See existing tests in ```test``` directory as an example. More expectations and examples on how to use Jasmine can be found on the official [documentation](http://jasmine.github.io/2.2/introduction.html).

**Build**

Run the build with the following command:

```
gulp
```

The build will:

1. Minify `awesomplete.js` and generate `awesomplete.min.js`.
2. Merge `awesomplete.base.css` and `awesomplete.theme.css` and generate `awesomplete.css`.