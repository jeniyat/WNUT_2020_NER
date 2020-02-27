The conll format:
=================================================
In `Conlll_Format` directory, there are multiple `phase_*` directories.  Each `phase_*` directory contains 10 protocols in the conll format. Each `*.txt` file contains annotations for one protocol. Each line is in the following format:

			<word>+"\t"+<NE>

The end of sentence is marked with an empty line.

The standoff format:
=================================================

In `Standoff_Format` directory, there are multiple `phase_*` directories.  Each `phase_*` directory contains 10 protocols in the standoff format.

Each text document in the dataset is acompanied by a corresponding annotation file. The two are associatied by using a simple file naming convention, wherein their base name (file name without the file extention) is the same: for example, the file protocol_30.ann contains annotations for the file protocol_30.txt.

Within the document, individual annotations are connected to specific spans of text through character offsets. For example, in a document beginning "Weigh 5.73 g of TCEP." the text "Weigh" is identified by the offset range 0..5. (All offsets all indexed from 0 and include the character at the start offset but exclude the character at the end offset.)

## Text file:

Text files are expected to have the file extension .txt and contain the text of the original protocol input into the system.

			How to Make a 0.5M TCEP Stock Solution
			Weigh 5.73 g of TCEP.
			Add 35 ml of cold molecular biology grade water to the vial, and dissolve the TCEP.
			This resulting solution is very acidic, with an approximate pH of 2.5.

The protocol texts are stored in plain text files encoded using UTF-8 (an extension of ASCII — plain ASCII texts work too). The Protocol texts contain newlines, each line indicating a single step in the protocol. The first line is always the protocol's name/title, as shown in the example above.

## Annotation file:

Annotations are stored in files with the .ann file extension. The various annotation types that may be contained in these files are discussed in the following.

All annotations follow the same basic structure: Each line contains one annotation, and each annotation is given an ID that appears first on the line, separated from the rest of the annotation by a single TAB character. The rest of the structure varies by annotation type.

Examples of annotation for an entity "Reagent" (T1), an event trigger "Action" (T2), an event (E1) and a relation (R2) are shown in the following.

			T1	Reagent 111 130	fresh tissue sample
			T2	Action 199 204	Weigh
			E1	Action:T2 Acts-on:T4
			T3	Amount 219 227	50-100mg
			T4	Reagent 228 235	tissues
			T5	Action 289 294	mince
			E2	Action:T5 Acts-on:T6 Using:T10 Site:T8
			T6	Reagent 299 305	tissue
			T7	Modifier 311 328	very small pieces
			R2	Mod-Link Arg1:E2 Arg2:T7

In our annotated dataset, we only ever make use of three types of annotations, each associated with their annotation ID. Those annotation IDs are described below:

T: text-bound annotation

R: relation

E: event

Detailed descriptions of each of these types of annotations are given below.

### Text bound annotations:

Text-bound annotations are an important category of annotation related to both entity and event annotations. Text-bound annotation identifies a specific span of text and assigns it a type.

			T1	Reagent 111 130	fresh tissue sample
			T2	Action 199 204	Weigh

All text-bound annotations follow the same structure. As in all annotations, the ID occurs first and is delimited from the rest of the line with a TAB character. The primary annotation is given as a SPACE-separated triple (type, start-offset, end-offset). The start-offset is the index of the first character of the annotated span in the text (".txt" file), i.e. the number of characters in the document preceding it. The end-offset is the index of the first character after the annotated span. Thus, the character in the end-offset position is not included in the annotated span. For reference, the text spanned by the annotation is included, separated by a TAB character.

#### Entity annotations:

Each entity annotation has a unique ID and is defined by type (e.g. Reagent or Amount) and the span of characters containing the entity mention (represented as a "start end" offset pair).

			T1	Reagent 111 130	fresh tissue sample
			T3	Amount 219 227	50-100mg
			T4	Reagent 228 235	tissues

Each line contains one text-bound annotation identifying the entity mention in text.

#### Event annotations

Each event annotation has a unique ID and is defined by type, event trigger (the text stating the event) and arguments. We only have one type of event in our dataset, which is "Action"

			T2	Action 199 204	Weigh
			E1	Action:T2 Acts-on:T4

The event triggers, annotations marking the word or words stating each event, are text-bound annotations and their format is identical to that for entities. (The IDs of triggers occupy the same space as the IDs of entities, and these must not overlap.)

As for all annotations, the event ID occurs first, separated by a TAB character. The event trigger is specified as TYPE:ID and identifies the event type and its trigger through the ID. By convention, the event type is specified both in the trigger annotation and the event annotation. The event trigger is separated from the event arguments by SPACE. The event arguments are a SPACE-separated set of ROLE:ID pairs, where ROLE is one of the event- and task-specific argument roles (e.g. Acts-on, Creates, Site, etc) and the ID identifies the entity or event filling that role. Note that several events can share the same trigger and that while the event trigger should be specified first, the event arguments can appear in any order.

#### Relation annotations:

Binary relations have a unique ID and are defined by their type (e.g. Measure, Mod-Link) and their arguments. Relation arguments are always identified simply as Arg1 and Arg2.


			R2	Mod-Link Arg1:E2 Arg2:T7

The format is similar to that applied for events, with the exception that the annotation does not identify a specific piece of text expressing the relation ("trigger"): the ID is separated by a TAB character, and the relation type and arguments by SPACE.


