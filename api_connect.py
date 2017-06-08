

from __future__ import unicode_literals
import frappe

import json

import socket

from frappe.model.document import Document

class api_connect(Document):
	pass


@frappe.whitelist()
def create_faktur_pajak_purchase_invoice_on_submit(doc,method):
	if doc.faktur_pajak :
		patokan_fp = frappe.db.sql(""" 
				SELECT fp.`name`, fp.`is_used` FROM `tabFaktur Pajak` fp WHERE fp.`name`="{}" 

				""".format(doc.faktur_pajak),as_list=1)
			
		if patokan_fp :
			frappe.msgprint("Faktur Pajak "+str(doc.faktur_pajak)+" sudah dibuat sebelumnya !")
		else :

			pr_doc = frappe.new_doc("Faktur Pajak")
			pr_doc.update({
				"no_faktur": str(doc.faktur_pajak),
				"is_used": 1
			})

			pr_doc.flags.ignore_permissions = 1
			pr_doc.save()

			frappe.msgprint("Faktur Pajak "+str(doc.faktur_pajak)+" created !")


@frappe.whitelist()
def update_faktur_pajak_sales_invoice_on_submit(doc,method):
	if doc.faktur_pajak :
		frappe.db.sql ("""
			update 
			`tabFaktur Pajak` 
			set 
			is_used= 1
			where 
			name="{0}"
		""".format(str(doc.faktur_pajak)))


@frappe.whitelist()
def update_faktur_pajak_sales_invoice_on_cancel(doc,method):
	if doc.faktur_pajak :
		frappe.db.sql ("""
			update 
			`tabFaktur Pajak` 
			set 
			is_used= 0
			where 
			name="{0}"
		""".format(str(doc.faktur_pajak)))

def check_item_unique(doc,method):
	check_size = check_type = check_color = check_product_group = check_item_group = check_extra = check_brand = ""
	if doc.size is None:
		check_size = """ size IS NULL AND """
	else:
		check_size = """ size = "{}" AND """.format(doc.size)

	if doc.type is None:
		check_type = """ type IS NULL AND """
	else:
		check_type = """ type = "{}" AND """.format(doc.type)

	if doc.color is None:
		check_color = """ color IS NULL AND """
	else:
		check_color = """ color = "{}" AND """.format(doc.color)

	if doc.product_group is None:
		check_product_group = """ product_group IS NULL AND """
	else:
		check_product_group = """ product_group = "{}" AND """.format(doc.product_group)

	if doc.item_group is None:
		check_item_group = """ item_group IS NULL AND """
	else:
		check_item_group = """ item_group = "{}" AND """.format(doc.item_group)

	if doc.extra is None:
		check_extra = """ extra IS NULL AND """
	else:
		check_extra = """ extra = "{}" AND """.format(doc.extra)

	if doc.brand is None:
		check_brand = """ brand IS NULL  """
	else:
		check_brand = """ brand = "{}"  """.format(doc.brand)

	result = frappe.db.sql(""" SELECT COUNT(name) FROM `tabItem` WHERE {}{}{}{}{}{}{} AND name!= "{}" """.format(check_size,check_type,check_color,check_product_group,check_item_group,check_extra,check_brand,doc.item_code),as_list=1)
	# frappe.throw(""" SELECT COUNT(name) FROM `tabItem` WHERE {}{}{}{}{}{}{}""".format(check_size,check_type,check_color,check_product_group,check_item_group,check_extra,check_brand))
	if result[0][0] > 0:
		# frappe.throw("Terdapat item yang memiliki spesifikasi yang sama dengan item yang baru. Silahkan merevisi spesifikasi item yang sedang anda buat.")
		pass
	