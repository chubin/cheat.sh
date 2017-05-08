describe("awesomplete.previous", function () {

	$.fixture("plain");

	subject(function () {
		return new Awesomplete("#plain", { list: ["item1", "item2", "item3"] });
	});

	def("lastIndex", function () { return this.subject.ul.children.length - 1 });

	describe("without any items found", function () {
		beforeEach(function () {
			$.type(this.subject.input, "nosuchitem");
			this.subject.open();
		});

		it("does not select any item", function () {
			this.subject.previous();
			expect(this.subject.index).toBe(-1);
		});
	});

	describe("with some items found", function () {
		beforeEach(function () {
			$.type(this.subject.input, "ite");
			this.subject.open();
		});

		describe("and no item was already selected", function () {
			it("selects the last item ", function () {
				this.subject.previous();
				expect(this.subject.index).toBe(this.lastIndex);
			});
		});

		describe("and some item was already selected", function () {
			it("selects the second item from the end", function () {
				this.subject.goto(this.lastIndex);
				this.subject.previous();
				expect(this.subject.index).toBe(this.lastIndex - 1);
			});

			it("selects the first item", function () {
				this.subject.goto(1);
				this.subject.previous();
				expect(this.subject.index).toBe(0);
			});

			it("selects the last item after reaching the start", function () {
				this.subject.goto(0);
				this.subject.previous();
				expect(this.subject.index).toBe(this.lastIndex);
			});
		});
	});
});
