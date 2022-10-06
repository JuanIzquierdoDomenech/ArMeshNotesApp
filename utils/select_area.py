from models.area_selection_model import AreaSelection, NormalDir, getPlaneFromString
from models.note_model import Note


def get_notes_inside_area(notes: list[Note], area: AreaSelection) -> list[Note]:

    notes_in_area = []

    for note in notes:
        # Cache current note x, y and z position
        note_x = note.info.position.x
        note_y = note.info.position.y
        note_z = note.info.position.z

        # Retrieve normal plane of selection
        normal_plane = getPlaneFromString(area.normalDir)

        # If the normal plane selected is X
        if normal_plane == NormalDir.NEGATIVE_X or normal_plane == NormalDir.POSITIVE_X:
            ########## X PLANE ##########
            # Calculate the tolerance in X (i.e., threshold to add to the X area of selection)
            tolerance_x = (note_x - area.tolerance, note_x + area.tolerance)
            if note_x > tolerance_x[0] and note_x < tolerance_x[1]:
                # We cannot rely that "begin" values will be lower given the 2 different signs, and the direction of the drawing
                min_y = min(area.begin.y, area.end.y)
                max_y = max(area.begin.y, area.end.y)
                min_z = min(area.begin.z, area.end.z)
                max_z = max(area.begin.z, area.end.z)
                if (note_y > min_y and note_y < max_y) and (
                    note_z > min_z and note_z < max_z
                ):
                    notes_in_area.append(note)

        elif (
            normal_plane == NormalDir.NEGATIVE_Y or normal_plane == NormalDir.POSITIVE_Y
        ):
            ########## Y PLANE ##########
            tolerance_y = (note_y - area.tolerance, note_y + area.tolerance)
            if note_y > tolerance_y[0] and note_y < tolerance_y[1]:
                min_x = min(area.begin.x, area.end.x)
                max_x = max(area.begin.x, area.end.x)
                min_z = min(area.begin.z, area.end.z)
                max_z = max(area.begin.z, area.end.z)
                if (note_x > min_x and note_x < max_x) and (
                    note_z > min_z and note_z < max_z
                ):
                    notes_in_area.append(note)

        else:
            ########## Z PLANE ##########
            tolerance_z = (note_z - area.tolerance, note_z + area.tolerance)
            if note_z > tolerance_z[0] and note_z < tolerance_z[1]:
                min_x = min(area.begin.x, area.end.x)
                max_x = max(area.begin.x, area.end.x)
                min_y = min(area.begin.y, area.end.y)
                max_y = max(area.begin.y, area.end.y)
                if (note_x > min_x and note_x < max_x) and (
                    note_y > min_y and note_y < max_y
                ):
                    notes_in_area.append(note)

    return notes_in_area
