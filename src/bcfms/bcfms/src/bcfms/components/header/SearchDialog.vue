<script setup lang="ts">
import { ref } from "vue";
import { useGettext } from "vue3-gettext";

import Button from "primevue/button";
import Dialog from "primevue/dialog";

const { $gettext } = useGettext();

const visible = ref(false);
const toggleModal = () => {
    visible.value = !visible.value;
};
</script>

<template>
    <Button
        icon="pi pi-search"
        :label="$gettext('Search')"
        @click="toggleModal"
    />

    <Dialog
        v-model:visible="visible"
        position="top"
        :header="$gettext('Search')"
        :dismissable-mask="true"
        :close-on-escape="true"
        :modal="true"
        :pt="{
            content: {
                style: {
                    padding: 0,
                    overflow: 'visible',
                },
            },
            root: {
                class: 'basic-search-dialog',
            },
        }"
        :show-header="false"
    >
        <div style="width: 80vw">
        </div>
    </Dialog>
</template>

<!-- NOT scoped because dialog gets appended to <body> and is unreachable via scoped styles -->
<style>
.basic-search-dialog {
    margin-top: 6rem !important;
    border-radius: 0 !important;
}

@media screen and (max-width: 960px) {
    .basic-search-dialog {
        margin-top: 1rem !important;
    }
}
</style>
