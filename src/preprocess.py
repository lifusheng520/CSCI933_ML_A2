import json
import re
from collections import defaultdict
from config import PLAY_FILES
from preprocess_config import *

# ----------------------------------------------------------------------
# Specific corrections based on utterance_id or speaker
# ----------------------------------------------------------------------

def apply_corrections(data, play_key):
    """
    Apply all manual corrections to utterances before cleaning.
    Modifies data in place.
    """
    # Helper to find an utterance by id
    utterance_map = {}
    for scene in data["scenes"]:
        for utt in scene["utterances"]:
            utterance_map[utt["utterance_id"]] = utt

    # Track previous utterance for inherited corrections
    prev_utt = None

    # First pass: apply corrections that depend on previous utterance
    for scene in data["scenes"]:
        scene_id = scene["scene_id"]
        for utt in scene["utterances"]:
            utt_id = utt["utterance_id"]

            # ========== Handle specific utterance IDs ==========

            # ALARUMS, ELSINORE, DUNSINANE, FIFE, FLOURISH, FORRES, INVERNESS, MANTUA, MUSIC, RETREAT, THUNDER
            if utt["speaker"] in ["ALARUMS", "ELSINORE", "FIFE", "FLOURISH", "FORRES", "INVERNESS", "MANTUA", "MUSIC", "RETREAT", "THUNDER"]:
                # Prepend speaker_original (or speaker) to text
                prefix = utt.get("speaker_original", utt["speaker"])
                if prefix:
                    new_text = f"{prefix}. {utt['text']}" if utt['text'] else prefix
                else:
                    new_text = utt['text']
                utt["text"] = new_text
                utt["speaker"] = "STAGE_DIRECTION"
                utt["speaker_original"] = "STAGE_DIRECTION"
                continue

            # Special cases for DUNSINANE (Macbeth)
            if utt["speaker"] == "DUNSINANE":
                if utt_id == "macbeth_5_1_0001":
                    utt["text"] = "Dunsinane. Anteroom in the castle."
                elif utt_id == "macbeth_5_3_0001":
                    utt["text"] = "Dunsinane. A room in the castle."
                elif utt_id == "macbeth_5_5_0001":
                    utt["text"] = "Dunsinane. Within the castle."
                elif utt_id == "macbeth_5_6_0001":
                    utt["text"] = "Dunsinane. Before the castle."
                elif utt_id == "macbeth_5_7_0001":
                    utt["text"] = "Dunsinane. Before the castle.  Alarums."
                utt["speaker"] = "STAGE_DIRECTION"
                utt["speaker_original"] = "STAGE_DIRECTION"
                continue

            # BAL -> BALTHASAR
            if utt["speaker"] == "BAL":
                utt["speaker"] = "BALTHASAR"
                utt["speaker_original"] = "BALTHASAR"

            # BOTH - handle by utterance_id as per instructions
            if utt["speaker"] == "BOTH":
                if play_key == "hamlet":
                    if scene_id == "hamlet_1_2":
                        utt["speaker"] = "MARCELLUS AND BERNARDO"
                        utt["speaker_original"] = "Mar and Ber"
                    elif scene_id == "hamlet_1_5":
                        utt["speaker"] = "MARCELLUS AND HORATIO"
                        utt["speaker_original"] = "Mar and Hor"
                    elif scene_id in ["hamlet_2_2", "hamlet_3_2", "hamlet_3_3"]:
                        utt["speaker"] = "ROSENCRANTZ AND GUILDENSTERN"
                        utt["speaker_original"] = "Ros and Guil"

            # COME (Hamlet)
            if utt_id == "hamlet_5_2_0111":
                utt["speaker"] = "HAMLET"
                utt["speaker_original"] = "Ham"
                utt["text"] = "Come. (They play.) Another hit. What say you?"

            # DRABBING (Hamlet)
            if utt_id == "hamlet_2_1_0012":
                utt["speaker"] = "POLONIUS"
                utt["speaker_original"] = "Pol"
                utt["text"] = "Drabbing. You may go so far."

            # FAREWELL, ON FORTINBRAS (Hamlet), GOOD PRUDENCE (Romeo and Juliet) - inherit from previous utterance
            if utt["speaker"] in ["FAREWELL","GOOD PRUDENCE","ON FORTINBRAS"]:
                if prev_utt:
                    prefix = utt.get("speaker_original", utt["speaker"])
                    if prefix:
                        new_text = f"{prefix}. {utt['text']}" if utt['text'] else prefix
                    else:
                        new_text = utt['text']
                    utt["text"] = new_text
                    utt["speaker"] = prev_utt["speaker"]
                    utt["speaker_original"] = prev_utt["speaker_original"]

            # FOR -> FORTINBRAS
            if utt["speaker"] == "FOR":
                utt["speaker"] = "FORTINBRAS"
                utt["speaker_original"] = "Fortinbras"

            # LAUR -> FRIAR LAURENCE
            if utt["speaker"] == "LAUR":
                utt["speaker"] = "FRIAR LAURENCE"
                utt["speaker_original"] = "Friar"

            # LUC -> LUCIANUS
            if utt["speaker"] == "LUC":
                utt["speaker"] = "LUCIANUS"
                utt["speaker_original"] = "Lucianus"

            # M (Romeo and Juliet)
            if utt["speaker"] == "M":
                if utt_id == "romeo_and_juliet_1_1_0061":
                    utt["speaker"] = "MONTAGUE'S WIFE"
                    utt["speaker_original"] = "Wife"
                    utt["text"] = "Thou shalt not stir one foot to seek a foe."
                elif utt_id == "romeo_and_juliet_1_1_0067":
                    utt["speaker"] = "MONTAGUE'S WIFE"
                    utt["speaker_original"] = "Wife"
                    utt["text"] = "O, where is Romeo? Saw you him to-day? Right glad I am he was not at this fray."

            # MESS -> MESSENGER
            if utt["speaker"] == "MESS":
                utt["speaker"] = "MESSENGER"
                utt["speaker_original"] = "Messenger"

            # OTHER -> OTHER CLOWN
            if utt["speaker"] == "OTHER":
                utt["speaker"] = "OTHER CLOWN"
                utt["speaker_original"] = "Other Clown"

            # PAR -> PARIS
            if utt["speaker"] == "PAR":
                utt["speaker"] = "PARIS"
                utt["speaker_original"] = "Paris"

            # PET -> PETER
            if utt["speaker"] == "PET":
                utt["speaker"] = "PETER"
                utt["speaker_original"] = "Peter"

            # PRO -> PROLOGUE
            if utt["speaker"] == "PRO":
                utt["speaker"] = "PROLOGUE"
                utt["speaker_original"] = "Prologue"

            # SERV -> SERVANT
            if utt["speaker"] == "SERV":
                utt["speaker"] = "SERVANT"
                utt["speaker_original"] = "Servant"

            # THIRD -> THIRD WITCH
            if utt["speaker"] == "THIRD":
                utt["speaker"] = "THIRD WITCH"
                utt["speaker_original"] = "THIRD WITCH"

            # VOLT -> VOLTEMAND
            if utt["speaker"] == "VOLT":
                utt["speaker"] = "VOLTEMAND"
                utt["speaker_original"] = "Voltemand"

            # WIFE -> CAPULET'S WIFE (Romeo and Juliet)
            if utt["speaker"] == "WIFE" and play_key == "romeo_and_juliet":
                utt["speaker"] = "CAPULET'S WIFE"
                utt["speaker_original"] = "Lady Capulet"

            # Additional specific utterance corrections
            if utt_id == "romeo_and_juliet_4_4_0012":
                utt["speaker"] = "CAPULET"
                utt["speaker_original"] = "Cap"

            # Hamlet 4.7 letter reading lines
            if utt_id in ["hamlet_4_7_0015", "hamlet_4_7_0016", "hamlet_4_7_0017", "hamlet_4_7_0018", "hamlet_4_7_0019", "hamlet_2_2_0026", "hamlet_2_2_0027"]:
                utt["speaker"] = "CLAUDIUS"
                utt["speaker_original"] = "King"

            if utt_id == "hamlet_4_7_0020":
                prefix = utt.get("speaker_original", utt["speaker"])
                if prefix:
                    new_text = f"{prefix}. {utt['text']}" if utt['text'] else prefix
                else:
                    new_text = utt['text']
                utt["text"] = new_text
                utt["speaker"] = "CLAUDIUS"
                utt["speaker_original"] = "King"

            # Also handle FLOURISH removal of specific utterance
            if utt_id == "macbeth_5_9_0017" and utt["speaker"] == "FLOURISH":
                # Mark for removal later by setting speaker to a special value
                utt["speaker"] = "REMOVE_ME"

            # Update previous utterance for inheritance
            prev_utt = utt

    # Second pass: remove utterances that are marked for removal (e.g., FLOURISH at the end)
    for scene in data["scenes"]:
        scene["utterances"] = [utt for utt in scene["utterances"] if utt.get("speaker") != "REMOVE_ME"]

    return data


def is_invalid_utterance(utt):
    """Return True if the utterance should be removed."""
    speaker = utt.get("speaker", "")
    text = utt.get("text", "")

    # Remove by exact speaker match
    if speaker in INVALID_SPEAKERS:
        return True
    
    # Remove copyright patterns from text
    new_text = text
    for pat in COPYRIGHT_PATTERNS:
        new_text = re.sub(pat, "", new_text, flags=re.IGNORECASE | re.DOTALL)
    new_text = new_text.strip()

    # Remove completely empty text
    if not new_text.strip():
        return True
    
    utt["text"] = new_text

    return False


def clean_utterances(utterances):
    """Return a list of utterances with invalid ones removed."""
    return [utt for utt in utterances if not is_invalid_utterance(utt)]


def regenerate_scene_text(scene):
    """Rebuild the 'text' field of a scene from its cleaned utterances."""
    lines = []
    for utt in scene["utterances"]:
        speaker = utt.get("speaker", "")
        text = utt.get("text", "")
        if speaker and speaker != "STAGE_DIRECTION":
            lines.append(f"{speaker}. {text}")
        else:
            lines.append(text)
    return "\n".join(lines)


def enhance_scene_summary(scene):
    """Create a more detailed scene summary."""
    scene_id = scene.get("scene_id")
    new_summary = scene.get("scene_summary")
    if scene_id in IMPROVED_HAMLET_SUMMARIES:
        new_summary = IMPROVED_HAMLET_SUMMARIES[scene_id]
    elif scene_id in IMPROVED_MACBETH_SUMMARIES:
        new_summary = IMPROVED_MACBETH_SUMMARIES[scene_id]
    elif scene_id in IMPROVED_ROMEO_AND_JULIET_SUMMARIES:
        new_summary = IMPROVED_ROMEO_AND_JULIET_SUMMARIES[scene_id]
    return new_summary


def clean_scene(scene):
    """Clean one scene and update its fields."""
    scene["utterances"] = clean_utterances(scene["utterances"])
    scene["text"] = regenerate_scene_text(scene)
    original_scene_summary = scene["scene_summary"]
    scene["original_scene_summary"] = original_scene_summary
    scene["scene_summary"] = enhance_scene_summary(scene)
    for utt in scene["utterances"]:
        utt["scene_summary"] = scene["scene_summary"]
    return scene

def parse_utterances_from_text(scene_text, act, scene, scene_summary, keywords, location):
    """Parse a raw scene text into utterances with speakers."""
    utterances = []
    lines = scene_text.strip().split('\n')
    
    utterance_counter = 1
    current_speaker = None
    current_text = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Check if line starts with a speaker name (uppercase, followed by period or space)
        # Pattern: SPEAKER. text or SPEAKER text
        match = re.match(r'^([A-Z][A-Z_\s]+)\.?\s+(.*)$', line)
        
        if match:
            # Save previous utterance if exists
            if current_speaker and current_text:
                utterance_id = f"macbeth_{act}_{scene}_{utterance_counter:04d}"
                utterances.append({
                    "speaker": current_speaker,
                    "speaker_original": current_speaker,
                    "text": ' '.join(current_text),
                    "utterance_id": utterance_id,
                    "source_id": utterance_id,
                    "play": "Macbeth",
                    "act": act,
                    "scene": scene,
                    "location": location,
                    "scene_summary": scene_summary,
                    "keywords": keywords
                })
                utterance_counter += 1
                current_text = []
            
            # Start new utterance
            current_speaker = match.group(1).strip()
            current_text.append(match.group(2).strip())
        elif current_speaker:
            # Continuation of previous speaker's lines
            current_text.append(line)
        else:
            # Stage direction or scene heading
            if line.startswith('[') or line.startswith('<'):
                speaker = "STAGE_DIRECTION"
                utterance_id = f"macbeth_{act}_{scene}_{utterance_counter:04d}"
                utterances.append({
                    "speaker": speaker,
                    "speaker_original": speaker,
                    "text": line,
                    "utterance_id": utterance_id,
                    "source_id": utterance_id,
                    "play": "Macbeth",
                    "act": act,
                    "scene": scene,
                    "location": location,
                    "scene_summary": scene_summary,
                    "keywords": keywords
                })
                utterance_counter += 1
    
    # Add the last utterance
    if current_speaker and current_text:
        utterance_id = f"macbeth_{act}_{scene}_{utterance_counter:04d}"
        utterances.append({
            "speaker": current_speaker,
            "speaker_original": current_speaker,
            "text": ' '.join(current_text),
            "utterance_id": utterance_id,
            "source_id": utterance_id,
            "play": "Macbeth",
            "act": act,
            "scene": scene,
            "location": location,
            "scene_summary": scene_summary,
            "keywords": keywords
        })
    
    return utterances

def rebuild_macbeth_act_1 (data):
    # Find Act 1, Scene 6
    scene_6_index = None
    for idx, scene in enumerate(data['scenes']):
        if scene['act'] == 1 and scene['scene'] == 6:
            scene_6_index = idx
            break

    if scene_6_index is not None:
        scene_6 = data['scenes'][scene_6_index]
        utterances = scene_6['utterances']
        
        # Find the problematic utterance
        for utt_idx, utt in enumerate(utterances):
            if 'SCENE VII' in utt['text']:
                original_text = utt['text']
                
                # Split at SCENE VII
                parts = original_text.split('SCENE VII')
                duncan_text = parts[0].strip()
                
                # Update the current utterance to only Duncan's text
                utt['text'] = duncan_text
                
                # Extract the remaining text after SCENE VII
                # The rest of the original text after the heading contains the lines for Scene 7
                if len(parts) > 1:
                    scene_7_raw_text = parts[1].strip()
                else:
                    # If no text after heading, look at following utterances
                    scene_7_raw_text = ''
                    for following in utterances[utt_idx + 1:]:
                        scene_7_raw_text += following['text'] + '\n'
                
                # Now, we need to collect ALL material that belongs to Act 1, Scene 7
                # This includes everything from the Sewer entrance through the end of the scene
                scene_7_lines = []
                
                # Add the stage direction for Sewer and servants
                scene_7_lines.append('[Enter a Sewer and divers Servants with dishes and service, who pass over the stage.  Then enter Macbeth.]')
                
                # Add Macbeth's soliloquy and the rest of the scene
                # Find the Macbeth soliloquy in the subsequent utterances
                macbeth_found = False
                for following in utterances[utt_idx + 1:]:
                    if 'Enter a Sewer and divers Servants with dishes and service, who' in following['text']:
                        continue
                    elif 'If it were done when \'tis done' in following['text']:
                        scene_7_lines.append(f"MACBETH. {following['text']}")
                        macbeth_found = True
                    elif following['speaker'] in ['LADY MACBETH', 'MACBETH'] and macbeth_found:
                        scene_7_lines.append(f"{following['speaker']}. {following['text']}")
                    elif following['speaker'] == 'STAGE_DIRECTION' and 'Enter' in following['text']:
                        scene_7_lines.append(f"[{following['text']}]")
                
                # Join all lines for Scene 7
                scene_7_text = '\n'.join(scene_7_lines)
                
                # Create new scene for Act 1, Scene 7
                new_scene_7 = {
                    "play": "Macbeth",
                    "act": 1,
                    "scene": 7,
                    "scene_id": "macbeth_1_7",
                    "location": "Macbeth's castle. Hautboys and torches",
                    "utterances": [],
                    "text": "",
                    "scene_summary": "",
                    "keywords": [
                        "ambition",
                        "guilt",
                        "persuasion"
                    ]
                }
                
                # Parse utterances from the scene text
                new_scene_7['utterances'] = parse_utterances_from_text(
                    scene_7_text, 1, 7, 
                    new_scene_7['scene_summary'], 
                    new_scene_7['keywords'],
                    new_scene_7['location']
                )
                new_scene_7['text'] = scene_7_text
                
                # Remove the utterances that belong to Scene 7 from Scene 6
                # Keep only utterances up to the point of the split
                utterances[utt_idx]['text'] = duncan_text
                # Remove following utterances that belong to Scene 7
                while len(utterances) > utt_idx + 1:
                    utterances.pop()
                
                # Renumber all utterances in Scene 6
                for new_idx, u in enumerate(utterances, start=1):
                    new_id = f"macbeth_1_6_{new_idx:04d}"
                    u['utterance_id'] = new_id
                    u['source_id'] = new_id
                
                # Rebuild Scene 6 text
                scene_6_lines = []
                for u in utterances:
                    if u['speaker'] == 'STAGE_DIRECTION':
                        scene_6_lines.append(f"[{u['text']}]")
                    else:
                        scene_6_lines.append(f"{u['speaker']}. {u['text']}")
                scene_6['text'] = '\n'.join(scene_6_lines)
                
                # Insert Scene 7 after Scene 6
                data['scenes'].insert(scene_6_index + 1, new_scene_7)
                break

    # Renumber all scene_ids after insertion to maintain order
    for idx, scene in enumerate(data['scenes']):
        # Only update scene_id if it follows the pattern
        if scene['scene_id'].startswith('macbeth_'):
            scene['scene_id'] = f"macbeth_{scene['act']}_{scene['scene']}"
        
        # Update utterance_id and source_id for all utterances in each scene
        for utt_idx, utt in enumerate(scene['utterances'], start=1):
            new_id = f"macbeth_{scene['act']}_{scene['scene']}_{utt_idx:04d}"
            utt['utterance_id'] = new_id
            utt['source_id'] = new_id

    return data


def clean_json_file(play_key, input_path, output_path):
    """Load JSON, apply corrections, clean scenes, save."""
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    data = apply_corrections(data, play_key)

    if play_key == "macbeth":
        data = rebuild_macbeth_act_1(data)

    # Clean each scene
    for scene in data["scenes"]:
        clean_scene(scene)    

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Cleaned {input_path} -> {output_path}")


# ----------------------------------------------------------------------
# Main execution
# ----------------------------------------------------------------------
if __name__ == "__main__":
    for play_key, file_name in PLAY_FILES.items():
        output_name = file_name.with_name(file_name.stem + "_cleaned" + file_name.suffix)
        clean_json_file(play_key, file_name, output_name)

    print("All files cleaned successfully.")