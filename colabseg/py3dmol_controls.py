#
# ColabSeg - Interactive segmentation GUI
#
# Marc Siggel, December 2021

import py3Dmol
import numpy as np


class seg_visualization(object):
    """docstring for JupyterFrontend."""

    def __init__(self, width=1000, height=500):
        super(seg_visualization, self).__init__()
        #self.view = py3Dmol.view(js="https://3dmol.org/build/3Dmol.js", width=width, height=height)
        self.view = py3Dmol.view(width=width, height=height)
        self.downsample = 1
    def view_update(self):
        """Update view of molecules"""
        self.view.update()
        return

    def view_zoomto(self):
        """zoomTo shortcut"""
        self.view.zoomTo()
        return

    def add_bounding_box(self, boxlength):
        """draws a bounding box according to the tomogram size"""
        # TODO add calculation of box size here
        x, y, z = boxlength
        self.view.addLine({ "color": 'red', "start": { "x": 0, "y": 0, "z": 0 }, "end": { "x": x, "y": 0, "z": 0} })
        self.view.addLine({ "color": 'green', "start": { "x": 0, "y": 0, "z": 0 }, "end": { "x": 0, "y": y, "z": 0} })
        self.view.addLine({ "color": 'blue', "start": { "x": 0, "y": 0, "z": 0 }, "end": { "x": 0, "y": 0, "z": z} })
        self.view.addLine({ "color": 'black', "start": { "x": x, "y": 0, "z": 0 }, "end": { "x": x, "y": y, "z": 0} })
        self.view.addLine({ "color": 'black', "start": { "x": 0, "y": y, "z": 0 }, "end": { "x": x, "y": y, "z": 0} })
        self.view.addLine({ "color": 'black', "start": { "x": x, "y": 0, "z": z }, "end": { "x": x, "y": y, "z": z} })
        self.view.addLine({ "color": 'black', "start": { "x": 0, "y": y, "z": z }, "end": { "x": x, "y": y, "z": z} })
        self.view.addLine({ "color": 'black', "start": { "x": 0, "y": 0, "z": z }, "end": { "x": x, "y": 0, "z": z} })
        self.view.addLine({ "color": 'black', "start": { "x": 0, "y": 0, "z": z }, "end": { "x": 0, "y": y, "z": z} })
        self.view.addLine({ "color": 'black', "start": { "x": x, "y": 0, "z": 0 }, "end": { "x": x, "y": 0, "z": z} })
        self.view.addLine({ "color": 'black', "start": { "x": 0, "y": y, "z": 0 }, "end": { "x": 0, "y": y, "z": z} })
        self.view.addLine({ "color": 'black', "start": { "x": x, "y": y, "z": 0 }, "end": { "x": x, "y": y, "z": z} })
    #    self.view.update()
        #self.view.zoomTo()
        self.view.addLabel("X", {"position": {"x": x, "y": 0, "z": 0},
                     "fontColor":"red",
                     "backgroundColor": "white",
                     "fontsize": 8,
                     "backgroundOpacity": "0.0",
                    })
        self.view.addLabel("Y", {"position": {"x": 0, "y": y, "z": 0},
                     "fontColor":"green",
                     "backgroundColor": "white",
                     "fontsize": 8,
                     "backgroundOpacity": "0.0",
                    })
        self.view.addLabel("Z", {"position": {"x": 0, "y": 0, "z": z},
                     "fontColor":"blue",
                     "backgroundColor": "white",
                     "fontsize": 8,
                     "backgroundOpacity": "0.0",
                    })
        return

    def load_all_models_from_file(self, file_list):
        """Load all xyz files from the xyz folder"""
        for file in file_list:
            load_model_from_file(file)
        return

    def load_model_from_file(self, filename):
        self.view.addModel(open(filename, 'r').read()[::self.downsample], 'xyz')
        self.view.setStyle({"sphere": {'color':'grey', "radius":"20","opacity":"0.6"}})
        self.view.zoomTo()
        self.view.update()
        return

    def load_all_models(self, cluster_list, start_index=0):
        """load all models from memory
            Use to initialize gui. Use to reload models after editing point cloud
        """
        for i, cluster_positions in enumerate(cluster_list):
            i = i + start_index
            xyz = self.make_xyz_string(cluster_positions[::self.downsample])
            self.view.addModel(xyz, 'xyz')
            self.view.setStyle({'model':i},{"sphere": {'color':'grey', "radius":"20","opacity":"0.6"}})
        self.view.zoomTo()
        return

    def load_all_models_fit(self, cluster_list, start_index):
        """load all fir models from memory
            Use to initialize gui. Use to reload models after editing point cloud
        """
        for i, cluster_positions in enumerate(cluster_list):
            i = i + start_index
            xyz = self.make_xyz_string(cluster_positions[::self.downsample])
            self.view.addModel(xyz, 'xyz')
            self.view.setStyle({'model':i},{"sphere": {'color':'blue', "radius":"20","opacity":"0.4"}})
        self.view.zoomTo()
        return

    def cluster_checkbox(self, cluster_index, state=False):
        """emphasize the view of the active segment cluster"""
        if state is False:
            cluster_selection_list[cluster_index] = False
            self.view.setStyle({'model':cluster_index},{"sphere": {'color':'grey', "radius":"10","opacity":"0.6"}})
            self.view.update()
        elif state is True:
            self.cluster_selection_list[cluster_index] = True
            self.view.setStyle({'model':cluster_index},{"sphere": {'color':'red', "radius":"10"}})
            self.view.update()
        return

    def highlight_cluster(self, cluster_index):
        """highlight cluster chosen with slider"""
        # NOTE old new are assigned by the slider widget
        if cluster_selection_list[cluster_index.old] == False:
            self.view.setStyle({'model':cluster_index.old},{"sphere": {'color':'grey', "radius":"10","opacity":"0.6"}})
        elif cluster_selection_list[cluster_index.old] == True:
            self.view.setStyle({'model':cluster_index.old},{"sphere": {'color':'red', "radius":"10"}})
        self.view.setStyle({'model':cluster_index.new},{"sphere": {'color':'yellow', "radius":"10"}})
        self.view.update()
        return

    def highlight_clusters(self, obj):
        """highlight cluster chosen with multi_select"""
        # NOTE old new are assigned by the slider widget
        for i in obj['old']:
            self.view.setStyle({'model':i},{"sphere": {'color':'grey', "radius":"20","opacity":"0.6"}})
        #    self.view.update()
        for j in obj['new']:
            self.view.setStyle({'model':j},{"sphere": {'color':'red', "radius":"20"}})
        #    self.view.update()
        self.view.update()
        return

    def highlight_fits(self, obj):
        """highlight RBF fit chosen with selector"""
        for i in obj['old']:
            self.view.setStyle({'model':i},{"sphere": {'color':'blue', "radius":"20","opacity":"0.4"}})
        #    self.view.update()
        for j in obj['new']:
            self.view.setStyle({'model':j},{"sphere": {'color':'blue', "radius":"20"}})
        self.view.update()
        return

    def update_highlight_clusters(self, indices):
        for i in indices:
            self.view.setStyle({'model':i},{"sphere": {'color':'grey', "radius":"20","opacity":"0.6"}})
            #self.view.update()
        for j in indices:
            self.view.setStyle({'model':j},{"sphere": {'color':'red', "radius":"20"}})
            #self.view.update()
        self.view.update()
        return

    def update_highlight_fits(self, indices):
        for i in indices:
            self.view.setStyle({'model':i},{"sphere": {'color':'blue', "radius":"20","opacity":"0.4"}})
            #self.view.update()
        for j in indices:
            self.view.setStyle({'model':j},{"sphere": {'color':'blue', "radius":"20"}})
            #self.view.update()
        self.view.update()
        return

    @staticmethod
    def make_xyz_string(point_cloud):
        """In memory XYZ string to load point cloud"""
        # TODO add variable step size
        xyz_string = "{}\n".format(len(np.asarray(point_cloud)[::10]))
        xyz_string += "pointcloud as xyz positions\n"
        for position in np.asarray(point_cloud)[::10]:
            xyz_string += "C {} {} {}\n".format(position[0], position[1], position[2])
        return xyz_string
