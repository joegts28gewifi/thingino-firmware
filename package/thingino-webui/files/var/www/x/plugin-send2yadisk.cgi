#!/bin/haserl
<%in _common.cgi %>
<%
plugin="yadisk"
plugin_name="Send to Yandex Disk"
page_title="Send to Yandex Disk"
params="enabled username password path socks5_enabled"

config_file="$ui_config_dir/$plugin.conf"
include $config_file

if [ "POST" = "$REQUEST_METHOD" ]; then
	# parse values from parameters
	read_from_post "$plugin" "$params"

	# validate
	if [ "true" = "$email_enabled" ]; then
		error_if_empty "$yadisk_username" "Yandex Disk username cannot be empty."
		error_if_empty "$yadisk_password" "Yandex Disk password cannot be empty."
	fi

	if [ -z "$error" ]; then
		tmp_file=$(mktemp)
		for p in $params; do
			echo "${plugin}_$p=\"$(eval echo \$${plugin}_$p)\"" >>$tmp_file
		done; unset p
		mv $tmp_file $config_file

		update_caminfo
		redirect_back "success" "$plugin_name config updated."
	fi

	redirect_to $SCRIPT_NAME
fi
%>
<%in _header.cgi %>

<form action="<%= $SCRIPT_NAME %>" method="post">
<% field_switch "yadisk_enabled" "Enable Yandex Disk bot" %>
<div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4 mb-4">
<div class="col">
<% field_text "yadisk_username" "Yandex Disk username" %>
<% field_password "yadisk_password" "Yandex Disk password" "A dedicated password for application. <a href=\"https://yandex.com/support/id/authorization/app-passwords.html\">Create it here</a>." %>
</div>
<div class="col">
<% field_text "yadisk_path" "Yandex Disk path" "$STR_SUPPORTS_STRFTIME" %>
<% field_switch "yadisk_socks5_enabled" "Use SOCKS5" "$STR_CONFIGURE_SOCKS5" %>
</div>
<div class="col">
<% ex "cat $config_file" %>
</div>
</div>
<% button_submit %>
</form>

<%in _footer.cgi %>
