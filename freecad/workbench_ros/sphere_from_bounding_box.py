import FreeCAD as fc
import FreeCADGui as fcgui

from PySide import QtCore  # FreeCAD's PySide!

from .dialogs import error_dialog


class SphereFromBoundingBox:
    def GetResources(self):
        return {'Pixmap': 'sphere_from_bbox',
                'MenuText': QtCore.QT_TRANSLATE_NOOP('workbench_ros', 'Sphere from bounding box'),  # TODO: translatable
                'ToolTip': QtCore.QT_TRANSLATE_NOOP('workbench_ros', 'Add a Part::Cube corresponding to the bounding box of the selected objects'),
                }

    def Activated(self):
        is_one_object_compatible = False
        for obj in fcgui.Selection.getSelection():
            has_bbox = False
            try:
                bbox = obj.Shape.BoundBox
            except AttributeError:
                has_bbox = True
            try:
                bbox = obj.Mesh.BoundBox
            except AttributeError:
                has_bbox = True
            if not has_bbox:
                continue
            is_one_object_compatible = True
            sphere_name = f'Bbox_{obj.Name}' if hasattr(obj, 'Name') else ''
            sphere = obj.Document.addObject('Part::Sphere', sphere_name)
            sphere.Radius = bbox.DiagonalLength / 2
            sphere.Placement.Base = bbox.Center
        if not is_one_object_compatible:
            error_dialog('No compatible object selected')

    def IsActive(self):
        return (fc.activeDocument() is not None)


fcgui.addCommand('SphereFromBoundingBox', SphereFromBoundingBox())
