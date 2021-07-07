{
   'name':" OKR",
   'author':"vvv",
   'category':"Sales",
   'summary':"""" OKR. """,
   'website':"vvv",
   'description':"""OKR.""" ,
   'version' : '14.0.1.0',
   'depends' : ['base','sale_management'],
   'data':[ 'security/ir.model.access.csv',
             #'security/okr_security.xml',
            'views/objective_view.xml',
            'views/key_result_view.xml',
            'views/okr_status_view.xml',
            'views/timesheet_view.xml',
              
          
  ],

    'installable':True,
    'application':True,
    'auto_install':False,
}
