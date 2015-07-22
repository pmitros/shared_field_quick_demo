"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String, RemoteScope, Boolean
from xblock.fragment import Fragment
from xblock.query import Shared


class SharedFieldDemoXBlock(XBlock):
    """
    TO-DO: document what your XBlock does.
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.

    count = Integer(
        default=0, scope=Scope.user_state,
        help="A simple counter, to show something happening",
        remote_scope = RemoteScope.user_state
    )

    text = String(
        default="", scope=Scope.user_state,
        help="A simple text string, to show something happening",
    )

    # init the int field query
    shared_num_query = Integer.Query(
        remote_scope = RemoteScope.user_state
    )

    # init the shared string field
    shared_num_shared = Shared(
        remote_scope = RemoteScope.user_state, 
        bind_attr = 'my_bind_func'
    )

    verifed_query = Boolean.Query(
        remote_scope = RemoteScope.user_state)

    @property
    def my_bind_func(self):
        self._update_test_user_id()
        return {'field_name':'count', 'user_id': self.test_user_id}

    def _update_test_user_id(self):
        self.test_user_id = '2'
        return self.test_user_id

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the SharedFieldDemoXBlock, shown to students
        when viewing courses.
        """
        # get the shared field data value
        # user_id ("2") is hard-coded
        self.user_id = self.scope_ids.user_id
        self.shared_num_query_value = self.shared_num_query.get(xblock=self, field_name = 'count', user_id='3')

        self.verifed_query_value = self.verifed_query.get(
            xblock=self, 
            field_name = 'verified', 
            user_id = 'student_1', 
            usage_id = 'toyverifyxblock.toy_verify.d0.u0')

        html = self.resource_string("static/html/shared_field_demo.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/shared_field_demo.css"))
        frag.add_javascript(self.resource_string("static/js/src/shared_field_demo.js"))
        frag.initialize_js('SharedFieldDemoXBlock')
        return frag

    # TO-DO: change this handler to perform your own actions.  You may need more
    # than one handler, or you may not need any handlers at all.
    @XBlock.json_handler
    def increment_count(self, data, suffix=''):
        """
        An example handler, which increments the data.
        """
        # Just to show data coming in...
        assert data['hello'] == 'world'

        self.count += 1

        # set the shared field data value
        # user selector ("2") is hard-coded
        self.shared_num_query.set(value=self.count, field_name='count', xblock=self, user_id="3")

        self.shared_num_shared = self.count
        
        return {"count": self.count}

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("SharedFieldDemoXBlock",
             """<vertical_demo>
                <shared_field_demo/>
                </vertical_demo>
             """),
        ]
