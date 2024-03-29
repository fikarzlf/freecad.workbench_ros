import FreeCAD as fc
import FreeCADGui as fcgui

from PySide import QtCore  # FreeCAD's PySide!

from .dialogs import error_dialog


class BoxFromBoundingBox:
    def GetResources(self):
        return {'Pixmap': 'box_from_bbox',
                'MenuText': QtCore.QT_TRANSLATE_NOOP('workbench_ros', 'Box from bounding box'),  # TODO: translatable
                'ToolTip': QtCore.QT_TRANSLATE_NOOP('workbench_ros', 'Add a Part::Cube corresponding to the bounding box of the selected objects'),
                }

    def Activated(self):
        is_one_object_compatible = False
        for obj in fcgui.Selection.getSelection():
            # Cf. https://github.com/pboechat/pyobb for oriented bounding-box.
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
            box_name = f'Bbox_{obj.Name}' if hasattr(obj, 'Name') else ''
            box = obj.Document.addObject('Part::Box', box_name)
            box.Length = bbox.XMax - bbox.XMin
            box.Width = bbox.YMax - bbox.YMin
            box.Height = bbox.ZMax - bbox.ZMin
            box.Placement.Base.x = bbox.XMin
            box.Placement.Base.y = bbox.YMin
            box.Placement.Base.z = bbox.ZMin
        if not is_one_object_compatible:
            error_dialog('No compatible object selected')

    def IsActive(self):
        return (fc.activeDocument() is not None)


fcgui.addCommand('BoxFromBoundingBox', BoxFromBoundingBox())
