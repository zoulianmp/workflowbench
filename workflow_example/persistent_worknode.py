#------------------------------------------------------------------------------
# Copyright (c) 2013, Nucleic Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#------------------------------------------------------------------------------
import cPickle

from atom.api import Unicode

from enaml.widgets.api import Container
from workflow.api import Worknode

import enaml
with enaml.imports():
    from persistent_view import PersistentManifest, create_new_area


print 'Imported Persistent Worknode!'


#: Storage for the pickled dock area. This would be saved
#: to some persistent storage media in a real application.
PICKLED_DOCK_AREA = None


class PersistentWorknode(Worknode):
    """ A custom Worknode class for the crash course example.

    """
    #: Storage for the plugin manifest's id.
    _manifest_id = Unicode()

    def start(self):
        """ Start the Worknode instance.

        This method will create the container content and register the
        provided plugin with the workbench.

        """
        self.content = Container(padding=0)
        self.load_area()
        manifest = PersistentManifest()
        self._manifest_id = manifest.id
        self.workbench.register(manifest)

    def stop(self):
        """ Stop the Worknode instance.

        This method will unregister the Worknode's plugin that was
        registered on start.

        """
        self.save_area()
        self.workbench.unregister(self._manifest_id)

    def save_area(self):
        """ Save the dock area for the Worknode.

        """
        global PICKLED_DOCK_AREA
        area = self.content.find('the_dock_area')
        PICKLED_DOCK_AREA = cPickle.dumps(area, -1)

    def load_area(self):
        """ Load the dock area into the Worknode content.

        """
        if PICKLED_DOCK_AREA is not None:
            area = cPickle.loads(PICKLED_DOCK_AREA)
        else:
            area = create_new_area()
        area.set_parent(self.content)
