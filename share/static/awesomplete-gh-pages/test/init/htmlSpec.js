describe("Html modifications", function () {

	$.fixture("plain");

	subject(function () { return new Awesomplete("#plain") });

	it("binds to correct input", function () {
		expect(this.subject.input instanceof HTMLElement).toBe(true);
		expect(this.subject.input.id).toBe("plain");
	});

	it("turns native autocompleter off", function () {
		expect(this.subject.input.getAttribute("autocomplete")).toBe("off");
	});

	describe("HTML tweaks", function () {
		it("creates container", function () {
			expect(this.subject.container instanceof HTMLElement).toBe(true);
			expect(this.subject.container.className).toBe("awesomplete");
		});

		it("places input inside container", function () {
			expect(this.subject.input.parentNode).toBe(this.subject.container);
		});

		it("creates list", function () {
			expect(this.subject.ul instanceof HTMLElement).toBe(true);
			expect(this.subject.ul.tagName).toBe("UL");
		});

		it("puts list inside container", function () {
			expect(this.subject.ul.parentNode).toBe(this.subject.container);
		});

		it("hides list", function () {
			expect(this.subject.ul.hasAttribute("hidden")).toBe(true);
		});
	});

	describe("ARIA support", function () {
		it("makes input accessible", function () {
			expect(this.subject.input.getAttribute("aria-autocomplete")).toBe("list");
		});

		it("creates status", function () {
			expect(this.subject.status instanceof HTMLElement).toBe(true);
			expect(this.subject.status.getAttribute("role")).toBe("status");
			expect(this.subject.status.getAttribute("aria-live")).toBe("assertive");
			expect(this.subject.status.getAttribute("aria-relevant")).toBe("additions");
		});

		it("puts status inside container", function () {
			expect(this.subject.status.parentNode).toBe(this.subject.container);
		});

		it("hides status", function () {
			expect(this.subject.status.className).toBe("visually-hidden");
		});
	});
});
