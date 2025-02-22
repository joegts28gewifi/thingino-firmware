#!/bin/haserl
<%in _common.cgi %>
<%
plugin="dusk2dawn"
plugin_name="Day/Night by Sun"
page_title="Dusk to Dawn"
params="enabled lat lng runat offset_sr offset_ss"

config_file="$ui_config_dir/$plugin.conf"
include $config_file

if [ "POST" = "$REQUEST_METHOD" ]; then
	# parse values from parameters
	read_from_post "$plugin" "$params"

	default_for "$dusk2dawn_runat" "0:00"
	default_for "$dusk2dawn_offset_sr" "0"
	default_for "$dusk2dawn_offset_ss" "0"

	# validate
	error_if_empty "$dusk2dawn_lat" "Latitude cannot be empty"
	error_if_empty "$dusk2dawn_lng" "Longitude cannot be empty"

	if [ -z "$error" ]; then
		tmp_file=$(mktemp)
		for p in $params; do
			echo "${plugin}_$p=\"$(eval echo \$${plugin}_$p)\"" >>$tmp_file
		done; unset p
		mv $tmp_file $config_file

		dusk2dawn > /dev/null

		update_caminfo
		redirect_back "success" "$plugin_name config updated."
	fi

	redirect_to $SCRIPT_NAME
else
	# Default values
	[ -z "$dusk2dawn_enabled" ] && dusk2dawn_enabled=false
	[ -z "$dusk2dawn_runat" ] && dusk2dawn_runat="0:00"
	[ -z "$dusk2dawn_offset_sr" ] && dusk2dawn_offset_sr="0"
	[ -z "$dusk2dawn_offset_ss" ] && dusk2dawn_offset_ss="0"
fi
%>
<%in _header.cgi %>

<form action="<%= $SCRIPT_NAME %>" method="post">
<div class="row g-4 mb-4">
<div class="col col-12 col-xl-4">
<% field_switch "dusk2dawn_enabled" "Enable dusk2dawn script" %>
<p><a href="https://my-coordinates.com/">Find your coordinates</a></p>
<%
field_text "dusk2dawn_lat" "Latitude"
field_text "dusk2dawn_lng" "Longitude"
field_text "dusk2dawn_offset_sr" "Sunrise offset, minutes"
field_text "dusk2dawn_offset_ss" "Sunset offset, minutes"
field_text "dusk2dawn_runat" "Run at"
%>
</div>
<div class="col col-12 col-xl-4">
<% ex "crontab -l" %>
</div>
<div class="col col-12 col-xl-4">
<% [ -f $config_file ] && ex "cat $config_file" %>
</div>
</div>

<% button_submit %>
</form>

<script>
function getCoordinates() {
	if ("geolocation" in navigator) {
		navigator.geolocation.getCurrentPosition((pos) => {
			$('#dusk2dawn_lat').value= pos.coords.latitude;
			$('#dusk2dawn_lng').value = pos.coords.longitude;
		}, function(error) {
			switch (error.code) {
				case error.PERMISSION_DENIED:
					console.error("The request for geolocation was denied.");
					break;
				case error.TIMEOUT:
					console.error("The request for geolocation timed out.");
					break;
				case error.POSITION_UNAVAILABLE:
					console.error("Location information is unavailable.");
					break;
				case error.UNKNOWN_ERROR:
					console.error("An unknown error occurred.");
					break;
			}
		});
	} else {
		alert("Geolocation is not available in this browser.");
	}
}
</script>

<%in _footer.cgi %>
