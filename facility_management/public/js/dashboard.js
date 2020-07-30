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

				frappe.model.with_doc("Dashboard Chart", chart.chart).then( chart_doc => {
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
				colors: [this.chart_doc.color || "light-blue"],
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
