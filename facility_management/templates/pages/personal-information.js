frappe.ready(function() {
  $('.btn-edit').click(() => {
    _prompt_edit_dialog();
  });
});

function _prompt_edit_dialog() {
  const d = new frappe.ui.Dialog({
    title: __("Edit Personal Information"),
    fields: [
      {
        label: __("CPR"),
        fieldname: 'cpr',
        fieldtype: 'Data',
        default: {{ data.cpr or '""' }},
      },
      {
        label: __("Passport No"),
        fieldname: 'passport_no',
        fieldtype: 'Data',
        default: {{ data.passport_no or '""' }},
      },
      {
        fieldname: 'cb',
        fieldtype: 'Column Break',
      },
      {
        label: __("Emergency Contact Name"),
        fieldname: 'emergency_contact_name',
        fieldtype: 'Data',
        default: {{ data.emergency_contact_name or '""' }},
      },
      {
        label: __("Mobile Number"),
        fieldname: 'mobile_no',
        fieldtype: 'Data',
        default: {{ data.mobile_no or '""' }},
      },
      {
        label: __("Mobile Number 2"),
        fieldname: 'mobile_no_2',
        fieldtype: 'Data',
        default: {{ data.mobile_no_2 or '""' }},
      },
      {
        label: __("Office Number"),
        fieldname: 'office_no',
        fieldtype: 'Data',
        default: {{ data.office_no or '""' }},
      },
      {
        label: __("Email Address"),
        fieldname: 'email',
        fieldtype: 'Data',
        default: {{ data.email or '""' }},
      },
      {
        fieldname: 'sb',
        fieldtype: 'Section Break',
      },
      {
        label: __("Employer Name"),
        fieldname: 'employer_name',
        fieldtype: 'Data',
        default: {{ data.employer_name or '""' }},
      },
      {
        label: __("Flat/Villa No"),
        fieldname: 'flat_villa_no',
        fieldtype: 'Data',
        default: {{ data.flat_villa_no or '""' }},
      },
      {
        label: __("Bldg Name"),
        fieldname: 'bldg_name',
        fieldtype: 'Data',
        default: {{ data.bldg_name or '""' }},
      },
      {
        label: __("Road No"),
        fieldname: 'road_no',
        fieldtype: 'Data',
        default: {{ data.road_no or '""' }},
      },
      {
        label: __("Road Name"),
        fieldname: 'road_name',
        fieldtype: 'Data',
        default: {{ data.road_name or '""' }},
      },
      {
        fieldname: 'cb',
        fieldtype: 'Column Break',
      },
      {
        label: __("Block No"),
        fieldname: 'block_no',
        fieldtype: 'Data',
        default: {{ data.block_no or '""' }},
      },
      {
        label: __("Area"),
        fieldname: 'area',
        fieldtype: 'Data',
        default: {{ data.area or '""' }},
      },
      {
        label: __("City"),
        fieldname: 'city',
        fieldtype: 'Data',
        default: {{ data.city or '""' }},
      },
    ],
    primary_action_label: __('Save'),
    primary_action: async (values) => {
      const response = await _edit_personal_info(values);
      if (response) {
        d.hide();
        frappe.msgprint("Personal info has been updated. Please refresh to see new changes.")
      }
    },
  });
  d.show();
}

async function _edit_personal_info(values) {
  const { message: response } = await frappe.call({
    method: 'facility_management.api.tenant_master.edit_personal_info',
    args: { data: values },
  });
  return response;
}
