// This file is part of the hBrowse software
// Copyright (c) CERN 2010
//
// Author: Lukasz Kokoszkiewicz [lukasz@kokoszkiewicz.com , lukasz.kokoszkiewicz@cern.ch]
//
// History:
// 19.09.2011 Created
//

// Load all required libraries
$LAB
// Load libs
.script('/templates/hbrowse2-common/lib/jquery-1.6.2.min.js')
.script('/templates/hbrowse2-common/lib/jquery.dataTables-1.9.0.min.js')
.script('/templates/hbrowse2-common/lib/Scroller.min.js')
.script('/templates/hbrowse2-common/lib/highcharts.js')
.script('/templates/hbrowse2-common/lib/exporting.js')
.script('/templates/hbrowse2-common/lib/quicksilver.js')
.script('/templates/hbrowse2-common/lib/jquery.livesearch.js')
.script('/templates/hbrowse2-common/lib/jquery.json-2.1.min.js')
.script('/templates/hbrowse2-common/lib/jquery.ba-bbq.min.js')
.script('/templates/hbrowse2-common/lib/cache.js')
.script('/templates/hbrowse2-common/lib/jquery.base64.js')
.script('/templates/hbrowse2-common/lib/jquery-ui-1.8.16.custom.min.js')
.script('/templates/hbrowse2-common/lib/jquery-ui-timepicker-addon.js')
.script('/templates/hbrowse2-common/lib/jquery.multiselect.min.js')
.script('/templates/hbrowse2-common/lib/jquery.dataTables.pagination.input.js')
//.script('media/lib/jquery.fixedheadertable.min.js')

// Load framework
.script('/templates/hbrowse2-common/scripts/api.js')
.script('/templates/hbrowse2-common/scripts/controlsupdate.js')
.script('/templates/hbrowse2-common/scripts/events.js')
.script('/templates/hbrowse2-common/scripts/controller.js')
.script('/templates/hbrowse2-common/scripts/data.js')
.script('/templates/hbrowse2-common/scripts/components/lkfw.searchable.list.js')
.script('/templates/hbrowse2-common/scripts/components/lkfw.datatable.js')
.script('/templates/hbrowse2-common/scripts/components/idfn.datatable.sorting.js')
.script('/templates/hbrowse2-common/scripts/components/lkfw.tooltip.js')

// Load Settings
.script('settings.js')

// Initialize hbrowse application
.wait(function(){
    $(document).ready( function() {
        var _cache_max_entries = 10;
        var _cache_lifetime = 60;
        _Cache = new Cache(_cache_max_entries, _cache_lifetime);
        Controller = new Controller();
        Controller.Init();
    } );
});
