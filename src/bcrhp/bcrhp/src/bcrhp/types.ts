import type { Ref } from "vue";
import type { TreeNode } from "primevue/treenode";
// import type { Label } from "@/arches_vue_utils/types";

// From arches_vue_utils in v8.0.x
export interface Language {
    code: string;
    default_direction: "ltr" | "rtl";
    id: number;
    isdefault: boolean;
    name: string;
    scope: string;
}

export interface Label {
    value: string;
    language_id: string;
    valuetype_id: string;
}

export interface WithLabels {
    labels: Label[];
}

export interface WithValues {
    values: Label[];
}

export type Labellable = WithLabels | WithValues;
// End copy from arches_vue_utils in v8.0.x

export interface User {
    first_name: string;
    last_name: string;
    username: string;
}

// Prop injection types
export interface UserRefAndSetter {
    user: Ref<User | null>;
    setUser: (userToSet: User | null) => void;
}
export interface DisplayedRowRefAndSetter {
    displayedRow: Ref<Concept | null>;
    setDisplayedRow: (val: Concept | Scheme | null) => void;
}

export interface Concept {
    id: string;
    labels: Label[];
    narrower: Concept[];
}

export interface Scheme {
    id: string;
    labels: Label[];
    top_concepts: Concept[];
}

export interface NodeAndParentInstruction {
    node: TreeNode;
    shouldHideSiblings: boolean;
}

export interface IconLabels {
    concept: string;
    scheme: string;
}

export interface SearchResultItem {
    id: string;
    labels: Label[];
    parents: {
        id: string;
        labels: Label[];
    }[];
    polyhierarchical: boolean;
}
