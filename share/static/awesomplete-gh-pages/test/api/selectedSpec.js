describe("awesomplete.selected", function () {

	$.fixture("plain");

	subject(function () {
		return new Awesomplete("#plain", { list: ["item1", "item2", "item3"] });
	});

	describe("with newly created completer", function () {
		it("is false", function () {
			expect(this.subject.selected).toBe(false);
		});
	});

	describe("with opened completer", function () {
		beforeEach(function () {
			this.subject.open();
			$.type(this.subject.input, "ite");
		});

		describe("and no item selected", function () {
			it("is false", function () {
				expect(this.subject.selected).toBe(false);
			});
		});

		describe("and some item selected", function () {
			it("is true", function () {
				this.subject.next();
				expect(this.subject.selected).toBe(true);
			});
		});
	});

	describe("with closed completer", function () {
		it("is false", function () {
			this.subject.close();
			expect(this.subject.selected).toBe(false);
		});
	});
});
