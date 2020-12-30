// Copyright (c) 2016, 9T9IT and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["FM Tenant"] = {
	"filters": [
        {
          fieldname: 'property_name',
          label: __('Name of the Property'),
          fieldtype: 'Link',
          options: 'Real Estate Property',
        },
        {
          fieldname: 'property_type',
          label: __('Property Type'),
          fieldtype: 'Select',
          options: '\nApartment\nVilla\nShop\nOffice',
        },
        {
          fieldname: 'property_no',
          label: __('Property Number'),
          fieldtype: 'Data',
        },
        {
          fieldname: 'tenant',
          label: __('Tenant'),
          fieldtype: 'Link',
          options: 'Tenant Master',
        },
        {
          fieldname: 'furnished',
          label: __('Type'),
          fieldtype: 'Select',
          options: '\nFully Furnished\nSemi Furnished\nUnfurnished'
        },
	]
}
