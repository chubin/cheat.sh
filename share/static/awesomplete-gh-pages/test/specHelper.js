fixture.setBase("test/fixtures");

// finds DOM elements in tests
function $ (str, context) {
	return (context || fixture.el).querySelector(str);
}

function $$ (str, context) {
	return (context || fixture.el).querySelectorAll(str);
}

// bundled fixture load/cleanup
$.fixture = function (fixtureName) {
	beforeEach(function () {
		// Awesomplete probably needs to cleanup this by itself
		try { Awesomplete.all = []; } catch(e) {};
		fixture.load(fixtureName + ".html");
	});

	afterEach(function () {
		fixture.cleanup();
	});
};

// spy to check if event was fired or not
$.spyOnEvent = function (target, type) {
	var handler = jasmine.createSpy(type);
	$.on(target, type, handler);
	return handler;
};

$.on = function (target, type, callback) {
	target.addEventListener(type, callback);
};

$.fire = function (target, type, properties) {
	var evt = document.createEvent("HTMLEvents");
	evt.initEvent(type, true, true );
	for (var j in properties) {
		evt[j] = properties[j];
	}
	target.dispatchEvent(evt);
	return evt;
};

// simulates text input (very simple, only "input" event is fired)
$.type = function (input, text) {
	input.focus();
	input.value = text;
	return $.fire(input, "input");
};

// simulates keydown events
$.keydown = function (target, keyCode) {
	return $.fire(target, "keydown", { keyCode: keyCode });
};
$.k = {
	ENTER: 13,
	ESC:   27,
	DOWN:  40,
	UP:    38
};

// $.noop returns a new empty function each time it's being called
Object.defineProperty($, "noop", {
	get: function () {
		return function noop () {}
	}
});
