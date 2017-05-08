describe("awesomplete.select", function () {

	$.fixture("plain");

	subject(function () {
		return new Awesomplete("#plain", { list: ["item1", "item2", "item3"] });
	});

	def("lastIndex", function () { return this.subject.ul.children.length - 1 });
	def("lastLi", function () { return this.subject.ul.children[this.lastIndex] });

	beforeEach(function () {
		$.type(this.subject.input, "ite");
	});

	describe("with closed completer", itDoesNotSelectAnyItem);

	describe("with opened completer", function () {
		beforeEach(function () {
			this.subject.open();
		});

		describe("and no current item", itDoesNotSelectAnyItem);

		describe("and current item", function () {
			beforeEach(function () {
				this.subject.goto(0);
			});

			itSelects("item1");
		});

		describe("and item specified as argument", function () {
			def("selectArgument", function () { return this.lastLi });

			itSelects("item3");
		});
	});

	// Shared behaviors

	function itSelects(expectedTxt) {
		it("fires awesomplete-select event", function () {
			var handler = $.spyOnEvent(this.subject.input, "awesomplete-select");
			this.subject.select(this.selectArgument);

			expect(handler).toHaveBeenCalledWith(
				jasmine.objectContaining({
					text: jasmine.objectContaining({ label: expectedTxt, value: expectedTxt }),
					origin: this.selectArgument || this.subject.ul.children[0]
				})
			);
		});

		describe("and awesomplete-select event was not prevented", function () {
			beforeEach(function () {
				$.on(this.subject.input, "awesomplete-select", $.noop);
			});

			it("changes the input value", function () {
				this.subject.select(this.selectArgument);
				expect(this.subject.input.value).toBe(expectedTxt);
			});

			it("closes completer", function () {
				spyOn(this.subject, "close");
				this.subject.select(this.selectArgument);

				expect(this.subject.close).toHaveBeenCalledWith({
					reason: "select"
				});
			});

			it("fires awesomplete-selectcomplete event", function () {
				var handler = $.spyOnEvent(this.subject.input, "awesomplete-selectcomplete");
				this.subject.select(this.selectArgument);

				expect(handler).toHaveBeenCalledWith(
					jasmine.objectContaining({
						text: jasmine.objectContaining({ label: expectedTxt, value: expectedTxt })
					})
				);
			});
		});

		describe("and awesomplete-select event was prevented", function () {
			beforeEach(function () {
				$.on(this.subject.input, "awesomplete-select", function (evt) { evt.preventDefault() });
			});

			it("does not change the input value", function () {
				this.subject.select(this.selectArgument);
				expect(this.subject.input.value).toBe("ite");
			});

			it("does not close completer", function () {
				spyOn(this.subject, "close");
				this.subject.select(this.selectArgument);

				expect(this.subject.close).not.toHaveBeenCalled();
			});

			it("does not fire awesomplete-selectcomplete event", function () {
				var handler = $.spyOnEvent(this.subject.input, "awesomplete-selectcomplete");
				this.subject.select(this.selectArgument);

				expect(handler).not.toHaveBeenCalled();
			});
		});
	}

	function itDoesNotSelectAnyItem() {
		it("does not change the input value", function () {
			this.subject.select();
			expect(this.subject.input.value).toBe("ite");
		});

		it("does not fire awesomplete-select event", function () {
			var handler = $.spyOnEvent(this.subject.input, "awesomplete-select");
			this.subject.select();

			expect(handler).not.toHaveBeenCalled();
		});

		it("does not fire awesomplete-selectcomplete event", function () {
			var handler = $.spyOnEvent(this.subject.input, "awesomplete-selectcomplete");
			this.subject.select();

			expect(handler).not.toHaveBeenCalled();
		});
	}
});
