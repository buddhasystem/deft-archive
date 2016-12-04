// This file is part of the TaskMonitoring software
//
// 
// 
//

function Settings() {

    function returnEmptyIfEmpty(val) {
        if (!val || val == 'unknown' || val == 'null' || val == 'panda0' || val == '-' ) {
            return '';
        }
        else {
            return val;
        }
    }
    
    // Application specific settings - START
    this.Application = {
        'userSelection': false, // Display user selection page? (true|false)
        'dataRefresh': true, // Display refresh dropdown field? (true|false)
        'timeRangeSelection': true, // Display time range dropdown field? (true|false)
        'jsonp': false, // allow requests to other hosts
        'pageTitle': 'DEFT', // Page title
//        'footerTxt': 'DEFT', // Footer text
        'supportLnk': 'https://twiki.cern.ch/twiki/bin/viewauth/AtlasComputing/DeftGui', // Link to support page
        'logoLnk': 'media/images/atlaslogo.png', // Link to page logo
        'usersListLbl': 'Users', // Label of user list search field, example: 'Users List'
        'mainsLbl': 'Meta-Tasks', // Name of mains content, example: 'Tasks'
        'subsLbL': 'Tasks', // Name of subs content, example: 'Jobs'
        'debugMode': true, // Display debug messages on errors inside dataTranslate functions? (true|false)
        'modelDefaults': function() { // Here You can set up model (data.js) default values
            return {
                'user': '',
                'refresh': 0,
                'table':'Mains',
                'initialTable': 'Mains',
                'p': 1,
                'sorting': [],
                'or': [], // opened table rows
                'uparam': [] // user defined params (for params that cannot be shared between use cases)
            };
        }
        // Optional init function alows to run some additional action on application initialization, it takes one parameter which is the state of the view (subs|mains|users)
        // Keep in mind the this is only the state of the url, not the state of the app, because of asyncronous ajax requests
        // the state of the view might be (temporarly) different then state of the url hash

      
        // Optional hash change function alows to react on hash changes, it takes one parameter which is the state of the view (subs|mains|users)
        // Keep in mind the this is only the state of the url, not the state of the app, because of asyncronous ajax requests
        // the state of the view might be (temporarly) different then state of the url hash
        /*'hashChangeEvent':function(appState) {
            alert(el);
        }*/
    };
    // Application specific settings - FINISH

    // Users list settings 
    this.Users = {
       
    };

    
    // Mains settings - START
    this.Mains = {
        'tableName': 'Meta -Tasks',
        'dataURL': 'data/metaData.json', // Mains URL for ajax request
        // Function, ajax request parameters
        // Input: Data - application Data model, rowDataSet - clicked row data (from ajax datatable response)
        'expandableRows':true, // If TRUE, rows will expand after clicking '+'
        'multipleER':false, // If TRUE, multiple rows can be expanded
        // Expanded data view setup object
        'expandData':{
            'dataURL': 'data/TaskData.json',
            'dataURL_params': function(Data, currentRow) {
                //alert(currentRow);
                obj = {
                    'what':'ALL',
                    'taskjobid':currentRow.TaskJobId,
                    'taskmonid':Data.filters.tid,
                    'type':'prod'
                };
                return obj;
            },

            'dataFunction': function(rowDataSet, jsonDataSet) {
            	 

                var html = '<p style="margin:0px; color:#1E4A68; font-weight:bold;text-align:center;font-size:11pt">&nbsp;AttemptNr</p>';
                var table = false;
                
                var tblData = Array();
                var Tasks = jsonDataSet.Tasks;
                
         
                for (var i=0;i<Tasks.length;i++) {
                    
                       
                    tblData.push([              
                                  
                   '<div class="wrapColumn"  title="'+Tasks[i].ID+'">'+Tasks[i].task_id+'</div>',                    

                   returnEmptyIfEmpty(Tasks[i].task_meta), ,
                    '<div class="status Status-'+ returnEmptyIfEmpty(Tasks[i].task_state) +'">' + returnEmptyIfEmpty(Tasks[i].task_state) + '</div>',
                    returnEmptyIfEmpty(Tasks[i].task_vo),
                    returnEmptyIfEmpty(Tasks[i].task_param),
                    returnEmptyIfEmpty(Tasks[i].task_transpath),
                    returnEmptyIfEmpty(Tasks[i].task_tag),
                    returnEmptyIfEmpty(Tasks[i].task_comment)
                   ])   
;
                }
                
                table = {
                    'tblLabels':['ID','METAID','STATE','VO','PARAMETERS','Transformation','Tag','Comment'],
                    'tblData':tblData
                };
                
                return [['table',table],['html',html]];
            }        	
        },
        'sorting':[0,'desc'], // [<column_index>,<sorting_direction>], sorting_direction='desc'||'asc'
        'iDisplayLength': 25, // Number of rows to display on single page
        'aLengthMenu':[10, 15, 20, 25, 30, 50, 100, 200],
        // Column labels (complex headers example)
        'tblLabels': ['METAID','TaskName','Comment','Requestor','Manager','VO','State','Request Time','Update Time'],
        'aoColumns': [
            /*ID*/{"sWidth":"130px","bSortable":false},
            /*TaskName*/{"sClass":"taskNameTd","sWidth":"100px"},
            /*Comment*/{"sClass":"numericTD", "fnRender":function(oObj){return '<a class="drilldown noJobsClick">'+oObj.aData[3]+'</a>';},"bUseRendered": false},
            /*Requestor*/{"sClass":"numericTD", "fnRender":function(oObj){return '<a class="drilldown noDefiClick">'+oObj.aData[4]+'</a>';},"bUseRendered": false},
            /*Manager*/{"sClass":"numericTD", "fnRender":function(oObj){return '<a class="drilldown noActiClick">'+oObj.aData[5]+'</a>';},"bUseRendered": false},
            /*VO*/{"sClass":"numericTD", "fnRender":function(oObj){return '<a class="drilldown noRunnClick">'+oObj.aData[6]+'</a>';},"bUseRendered": false},
            /*State*/{"sClass":"numericTD", "fnRender":function(oObj){return '<a class="drilldown noHoldClick">'+oObj.aData[7]+'</a>';},"bUseRendered": false},
            /*Request Time*/{"sClass":"numericTD" },
            /*Update Time*/{"sClass":"numericTD"}
        ],
        // Function: extracting array of data form Ajax response
        // Example:
        // - Ajax response: {'user_taskstable':[{col_val1, col_val2, ...}, ...]}
        // - Required function: function(data) { return data.user_taskstable; }
        'getDataArray': function(data) {

            return data.metaTasks;
        },
        // Function, translates ajax response onto dataTables plugin data format
        // Output: [[col_val1, col_val2, ...], ...]
        'translateData': function(dataJSON) {
            var tasksArr = Array();
            for (i in dataJSON) {
                tasksArr.push(Array(
                    //'<input class="resubmitCheckbox selectTask" type="checkbox" />',
                        /*ID*/(dataJSON[i].meta_id || ''),
                        /*TaskName*/returnEmptyIfEmpty(dataJSON[i].TASKNAME),
                        /*Comment*/(dataJSON[i].meta_comment || ''),
                        /*Requestor*/(dataJSON[i].meta_requestor || ''),
                        /*Manager*/(dataJSON[i].meta_manager || ''),
                        /*VO*/(dataJSON[i].meta_vo || ''),
                        /*State*/(dataJSON[i].meta_state ? '<div class="status Status-'+dataJSON[i].meta_state+'">'+dataJSON[i].meta_state+'</div>' : '<div class="status Unknown">Unknown</div>'),
                        /*Request Time*/(dataJSON[i].meta_req_ts || ''),
                        /*Update Time*/(dataJSON[i].meta_upd_ts || '')
                   
                ));
            }
            return tasksArr;
        },

        'drillDownHandler': function(Data, el, rowIndex) {
            var aClass = $(el).find('a').attr('class').replace("drilldown ","").replace(" taskname_toggle","");
            
            var classTranslate = {
                'tmIdClick':'all',
                'noJobsClick':'all',
                'noDefiClick':'defined',
                'noActiClick':'activated',
                'noRunnClick':'running',
                'noHoldClick':'holding',
                'noFiniClick':'finished',
                'noFailClick':'failed',
                'noCancClick':'cancelled',
                'noOtheClick':'others'
            };
            var status = classTranslate[aClass];
            var tid = Data.mem.table.data[rowIndex].TASKNAME;
            
            return {'table':'Jobs',filters:{'status':status,'tid':tid}};
        },
        'tableActivityEvent': function(el, dataMem) {
            $('.selectAll').click(function(){
                if ($(this).attr('checked') == 'checked')
                    $('.resubmitCheckbox').attr('checked','checked');
                else
                    $('.resubmitCheckbox').removeAttr('checked');
            });
            $('.resubmitAll').click(function(){
                $('#resubmitTable').dialog({ 
                    title: 'Message',
                    modal: true,
                    width: 900,
                    resizable: false,
			        buttons: {
				        Ok: function() {
					        $( this ).dialog( "close" );
				        }
			        } 
	            });
	            //alert(';)');
	            $('#fixedHeader').fixedHeaderTable({ footer: true, cloneHeadToFoot: true, fixedColumn: false });
            });
            
            $('#pattern').lkfw_tooltip({
                'content':{
                    'pattern':{ 'html':'Pattern string be used in SQL query to search tasks by specified taskname pattern. Wildcards characters can be used (&#42;) along with AND (&amp;&amp;) and OR (||). Example: " &#42;m716&#42; || &#42;Np5PDF&#42; "' }
                },
                'take':'id',
                'delay':0,
                'place':'bottom',
                'posShift':[-3,0],
                'classDist':'_tblHeaders'
            });

        },
        'filters':[
            {
                'label':'Pattern',  // String
                'urlVariable':'pattern',  // String - lower cased, no spaces, no special characters
                'fieldType':'text',  // String (text|select|multiselect|date)
                'value':'',
                'options':{}
            },
            {
                'label':'From',  // String
                'urlVariable':'from',  // String - lower cased, no spaces, no special characters
                'fieldType':'date',  // String (text|select|multiselect|date)
                'value':'',
                'options':{}
            },
            {
                'label':'Till',  // String
                'urlVariable':'till',  // String - lower cased, no spaces, no special characters
                'fieldType':'date',  // String (text|select|multiselect|date)
                'value':'',
                'options':{}
            },
            {
                'label':'Time Range',  // String
                'urlVariable':'timerange',  // String - lower cased, no spaces, no special characters
                'fieldType':'select',  // String (text|select|multiselect|date)
                'value':'lastDay',
                'options':{
                    'translateData': function(data) {
                        return [['lastDay','Last Day'],['last2Days','Last 2 Days'],['last3Days','Last 3 Days'],['lastWeek','Last Week'],['last2Weeks','Last 2 Weeks'],['lastMonth','Last Month']];
                    }
                }
            }
        ],
        'charts': [
            {
                'name':'Status Overview',
                'type':'hchart', // (gchart|hchart)
                'onDemand':false,
                // translates data onto requires format:
                // {"chd":"t:60,40","chl":"Hello|World"}
                'translateData':function(dataMem) {
                    var data = dataMem.table.data;
                    var dataLen = data.length;
                    
                    if (dataLen > 0) {
                        var obj = {
                            'statuses':['DEFINED','ACTIVATED','RUNNING','HOLDING','FINISHED','FAILED','CANCELLED','OTHERS'],
                            'statusesCnt':[0,0,0,0,0,0,0,0],
                            'statusesLbl':['Defined','Activated','Running','Holding','Finished','Failed','Cancelled','Others'],
                            'statusesColors':['#727272','#727272','#727272','#727272','#59D118','#c50000','#ffc000','#727272']
                        };
                        
                        for (var i=0; i<dataLen; i++) {
                            var row = data[i];
                            for (var j=0; j<obj.statuses.length; j++) {
                                obj.statusesCnt[j] += row[obj.statuses[j]];
                            }
                        }
                        
                        var data = [];
                        
                        for (var i=0;i<obj.statusesCnt.length;i++) {
                            if (obj.statusesCnt[i] > 0) {
                                if (obj.statuses[i] == 'FAILED') data.push({name:obj.statusesLbl[i]+' ('+obj.statusesCnt[i]+')',color:obj.statusesColors[i],y:obj.statusesCnt[i],sliced:true,selected:true});
                                else data.push({name:obj.statusesLbl[i]+' ('+obj.statusesCnt[i]+')',color:obj.statusesColors[i],y:obj.statusesCnt[i]});
                            }
                        }
                    } else return false;
                    
                    output = {
                        chart: {
                            height:400,
                            width:550,
                            backgroundColor:'#ffffff',
                            borderColor:'#aaaaaa',
                            borderWidth:1
                        },
                        title: {
                            text: 'Status Overview'
                        },
                        tooltip: {
                            formatter: function() {return '<b>'+ this.point.name +'</b>: '+ this.y;}
                        },
                        plotOptions: {
                            pie: {
                                allowPointSelect: true,
                                cursor: 'pointer'
                            }
                        },
                        series: [{
                            type: 'pie',
                            data: data
                        }]
                    };
                    
                    return output;
                }
            }
        ]
    };
    // User Meta-Tasks settings - FINISH
    
    // Jobs settings will be added here
  

}
