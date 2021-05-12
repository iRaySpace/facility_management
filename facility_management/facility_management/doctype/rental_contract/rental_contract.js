// Copyright (c) 2020, 9T9IT and contributors
// For license information, please see license.txt

frappe.ui.form.on('Rental Contract', {
  onload: function (frm) {
    frm.set_query('property', function () {
      return {
        filters: {
          rental_status: 'Vacant',
        },
      };
    });
  },
  refresh: function (frm) {
    _add_payment_entry(frm);
    _add_cancel_btn(frm);
    _set_items_read_only(frm);
    _add_refresh_btn(frm);
  },
  contract_start_date: function (frm) {
    _set_start_invoice_date(frm);
  },
  after_cancel: function (frm) {
    _set_cancellation(frm);
  },
});


frappe.ui.form.on('Rental Contract Item', {
  create_invoice: async function (frm, cdt, cdn) {
    const { message: result } = await frappe.call({
      method: 'facility_management.api.rental_contract.create_invoice',
      args: {
        rental: frm.doc.name,
        rental_item: cdn,
      },
    });
    if (result) {
      frappe.msgprint('Invoice has been created. Please refresh the page in order to view the changes.');
    }
  },
});


function _add_payment_entry(frm) {
  if (frm.doc.docstatus !== 0) {
    frm.add_custom_button(__('Add Payment Entry'), async function () {
      const { message: tenant_master } = await frappe.db.get_value(
        'Tenant Master',
        frm.doc.tenant,
        'customer',
      );
      // ! hax ! (manually doing the route options of core and timing)
      frappe.__route_options = {
        mode_of_payment: 'Cash',
        party_type: 'Customer',
        party: tenant_master.customer,
        paid_amount: frm.doc.rental_amount,
      };
      frappe.new_doc('Payment Entry');
    });
  }
}


function _add_cancel_btn(frm) {
  if (frm.doc.docstatus === 1) {
    // remove cancel button and add contract disable
    setTimeout(function () {
      frm.page.set_secondary_action('Contract Disable', function () {
        frappe.prompt(
          [
            {
              fieldname: 'cancellation_date',
              fieldtype: 'Date',
              label: 'Cancellation Date',
              description:
                'Set as empty if you want to cancel the Rental Contract now.',
            },
            {
              fieldname: 'reason_for_cancellation',
              fieldtype: 'Small Text',
              label: 'Reason for Cancellation',
            },
          ],
          function (values) {
            frm.__cancellation_date = values.cancellation_date;
            frm.__reason_for_cancellation = values.reason_for_cancellation;
            frm.savecancel();
          },
          'Rental Contract Cancel',
        );
      });
      frm.page.btn_secondary.addClass('btn-danger');
    }, 300);
  }
}

function _add_refresh_btn(frm) {
  if (frm.doc.docstatus === 1) {
    frm.add_custom_button(__("Refresh Invoice Description"), async function () {
      await frappe.call({
        method: 'facility_management.api.rental_contract.refresh_invoice_description',
        args: { rental_contract: frm.doc.name },
      });
      frm.reload_doc();
    });
  }
}

function _set_start_invoice_date(frm) {
  frm.set_value('start_invoice_date', frm.doc.contract_start_date);
}


function _set_items_read_only(frm) {
  frm.set_df_property('items', 'read_only', 1);
}


function _set_cancellation(frm) {
  frappe.call({
    method: 'facility_management.api.rental_contract.set_cancellation',
    args: {
      rental_contract: frm.doc.name,
      cancellation_date: frm.__cancellation_date || null,
      reason_for_cancellation: frm.__reason_for_cancellation || null,
    },
  });
}