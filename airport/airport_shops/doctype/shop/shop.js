// Copyright (c) 2025, Unity and contributors
// For license information, please see license.txt

frappe.ui.form.on("Shop", {
	refresh(frm) {
		// Filter shop_type link to show only enabled shop types
		frm.set_query('shop_type', function() {
			return {
				filters: {
					'enabled': 1
				}
			};
		});
	}
});
