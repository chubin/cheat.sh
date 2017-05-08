describe("Constructor options", function () {

	$.fixture("options");

	subject(function () { return new Awesomplete(this.element, this.options) });

	describe("with default options", function () {
		def("element", "#with-data-list");

		it("requires minimum 2 chars to open completer", function () {
			expect(this.subject.minChars).toBe(2);
		});

		it("shows 10 items in completer", function () {
			expect(this.subject.maxItems).toBe(10);
		});

		it("does not select the first ocurrence automatically" , function () {
			expect(this.subject.autoFirst).toBe(false);
		});

		it("modifies list item with DATA", function () {
			expect(this.subject.data).toBe(Awesomplete.DATA);
		});

		it("filters with FILTER_CONTAINS", function () {
			expect(this.subject.filter).toBe(Awesomplete.FILTER_CONTAINS);
		});

		it("orders with SORT_BYLENGTH", function () {
			expect(this.subject.sort).toBe(Awesomplete.SORT_BYLENGTH);
		});

		it("creates item with ITEM", function () {
			expect(this.subject.item).toEqual(Awesomplete.ITEM);
		});

		it("replaces input value with REPLACE", function () {
			expect(this.subject.replace).toEqual(Awesomplete.REPLACE);
		});
	});

	describe("with custom options in constructor", function () {
		def("element", "#with-data-list");
		def("options", function () {
			return {
				minChars: 3,
				maxItems: 9,
				autoFirst: true,
				filter: $.noop,
				sort: $.noop,
				item: $.noop,
				replace: $.noop
			};
		});

		it("overrides simple default options", function () {
			expect(this.subject.minChars).toBe(3);
			expect(this.subject.maxItems).toBe(9);
			expect(this.subject.autoFirst).toBe(true);
		});

		it("overrides default functions", function () {
			expect(this.subject.filter).toBe(this.options.filter);
			expect(this.subject.sort).toBe(this.options.sort);
			expect(this.subject.item).toBe(this.options.item);
			expect(this.subject.replace).toBe(this.options.replace);
		});
	});

	describe("with custom options in data-* attributes", function () {
		def("element", "#with-custom-options");

		it("overrides simple default options", function () {
			expect(this.subject.minChars).toBe(4);
			expect(this.subject.maxItems).toBe(8);
			expect(this.subject.autoFirst).toBe(true);
		});
	});
});
