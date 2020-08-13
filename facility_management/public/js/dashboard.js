// For version-12
// https://github.com/frappe/frappe/blob/version-12/frappe/core/page/dashboard/dashboard.js

frappe.pages['dashboard'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: __("Dashboard"),
		single_column: true
	});
	frappe.dashboard = new CustomDashboard(wrapper);
	$(wrapper).bind('show', function() {
		frappe.dashboard.show();
		const { dashboard_name } = frappe.dashboard;
		if (dashboard_name == 'Facility Management') {
            frappe.dashboard.page.add_menu_item('Filter', async function() {
                const filter_values = await _show_filter_dialog();
                apply_dashboard_filters(filter_values);
            });
		}
	});
}


class CustomDashboard extends Dashboard {
    refresh() {
        this.get_dashboard_doc().then((doc) => {
			this.dashboard_doc = doc;
			this.charts = this.dashboard_doc.charts;

			this.charts.map((chart) => {
				let chart_container = $("<div></div>");
				chart_container.appendTo(this.container);

				frappe.model.with_doc("Dashboard Chart", chart.chart).then(chart_doc => {
				    const filters = {
				        ...JSON.parse(chart_doc.filters_json),
				        ...frappe.dashboard.__global_filters,
				    };
				    chart_doc.filters_json = JSON.stringify(filters);
				    let dashboard_chart = new CustomDashboardChart(chart_doc, chart_container);
					dashboard_chart.show();
				});
			});
		});
    }
}


class CustomDashboardChart extends DashboardChart {
    render() {
		this.chart_container.find('.chart-loading-state').addClass('hide');
		if (!this.data) {
			this.chart_container.find('.chart-empty-state').removeClass('hide');
		} else {
			let chart_args = {
				title: this.chart_doc.chart_name,
				data: this.data,
				type: this.chart_doc.type.toLowerCase(),
				colors: ['#FFC108', '#2096F3', '#F44336', '#009588', '#04A9F4'],
				axisOptions: {
					xIsSeries: this.chart_doc.timeseries,
					shortenYAxisNumbers: 1
				}
			};
			if (!this.chart) {
				this.chart = new frappe.Chart(this.chart_container.find(".chart-wrapper")[0], chart_args);
			} else {
				this.chart.update(this.data);
			}
		}
    }
}


function _show_filter_dialog() {
    return new Promise(function(resolve, reject) {
        const filter_dialog = new frappe.ui.Dialog({
            title: 'Enter filters',
            fields: [
                {
                    fieldtype: 'Link',
                    fieldname: 'property_group',
                    label: 'Real Estate Property',
                    options: 'Real Estate Property',
                },
            ],
            primary_action_label: 'Filter',
            primary_action: function(values) {
                resolve(values);
                filter_dialog.hide();
            }
        });
        filter_dialog.show();
    });
}


function apply_dashboard_filters(filters) {
    frappe.dashboard.__global_filters = filters;
    frappe.dashboard.container.children().remove();
    frappe.dashboard.refresh();
}
