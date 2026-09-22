/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { useDropzone } from "@web/core/dropzone/dropzone_hook";
import { checkFileSize } from "@web/core/utils/files";
import { getDataURLFromFile } from "@web/core/utils/urls";
import { BinaryField, binaryField } from "@web/views/fields/binary/binary_field";

import { useRef } from "@odoo/owl";

/**
 * Binary field that also accepts a file dropped on it, on top of the regular
 * "Upload your file" button inherited from BinaryField. Everything the binary
 * widget offers — upload, download, edit, clear — is kept as it is.
 */
export class BinaryDropField extends BinaryField {
    static template = "algorid_binary_drop.BinaryDropField";
    static props = {
        ...BinaryField.props,
        dropHint: { type: String, optional: true },
        replaceHint: { type: String, optional: true },
    };

    setup() {
        super.setup();
        this.dropZoneRef = useRef("dropZone");
        useDropzone(
            this.dropZoneRef,
            (ev) => this.onDrop(ev),
            "o_algorid_binary_dropzone",
            () => !this.props.readonly
        );
    }

    get dropHint() {
        return this.props.dropHint || _t("or drop a file here");
    }

    get replaceHint() {
        return this.props.replaceHint || _t("or drop a file here to replace it");
    }

    /**
     * The accepted_file_extensions option, as a list. Null means "accept all".
     */
    get acceptedExtensions() {
        const accepted = this.props.acceptedFileExtensions;
        if (!accepted || accepted === "*") {
            return null;
        }
        return accepted
            .split(",")
            .map((ext) => ext.trim().toLowerCase())
            .filter(Boolean);
    }

    /**
     * The FileUploader filters on accepted_file_extensions and allowed_mime_type
     * for us, but a dropped file never goes through it, so both have to be
     * checked here.
     */
    isAcceptedFile(file) {
        const accepted = this.acceptedExtensions;
        if (!accepted) {
            return true;
        }
        const name = (file.name || "").toLowerCase();
        const type = (file.type || "").toLowerCase();
        return accepted.some((ext) => {
            if (ext.startsWith(".")) {
                return name.endsWith(ext);
            }
            if (ext.endsWith("/*")) {
                return type.startsWith(ext.slice(0, -1));
            }
            return type === ext;
        });
    }

    /**
     * Same whitelist check as FileUploader.validFileType, applied to the drop
     * path. Kept in sync with web/static/src/views/fields/file_handler.js.
     */
    isAllowedMIMEType(file) {
        const allowed = this.props.allowedMIMETypes;
        return !allowed || allowed.includes(file.type);
    }

    async onDrop(ev) {
        if (this.props.readonly) {
            return;
        }
        const file = ev.dataTransfer && ev.dataTransfer.files && ev.dataTransfer.files[0];
        if (!file) {
            return;
        }
        if (!this.isAcceptedFile(file)) {
            this.notification.add(_t("This file type is not accepted here."), { type: "danger" });
            return;
        }
        if (!this.isAllowedMIMEType(file)) {
            this.notification.add(
                _t("Oops! '%(fileName)s' didn’t upload since its format isn’t allowed.", {
                    fileName: file.name,
                }),
                { type: "danger" }
            );
            return;
        }
        if (!checkFileSize(file.size, this.notification)) {
            return;
        }
        if (!file.size) {
            this.notification.add(_t("There was a problem while uploading your file."), {
                type: "danger",
            });
            return;
        }
        const dataUrl = await getDataURLFromFile(file);
        await this.update({ data: dataUrl.split(",")[1], name: file.name });
    }
}

export const binaryDropField = {
    ...binaryField,
    component: BinaryDropField,
    displayName: _t("File (drag and drop)"),
    supportedOptions: [
        ...(binaryField.supportedOptions || []),
        {
            label: _t("Drop hint"),
            name: "drop_hint",
            type: "string",
            help: _t("Text shown under the upload button while the field is empty."),
        },
        {
            label: _t("Replace hint"),
            name: "replace_hint",
            type: "string",
            help: _t("Text shown under the file name once a file is set."),
        },
    ],
    extractProps: ({ attrs, options }, dynamicInfo) => ({
        ...binaryField.extractProps({ attrs, options }, dynamicInfo),
        dropHint: options.drop_hint,
        replaceHint: options.replace_hint,
    }),
};

registry.category("fields").add("binary_drop", binaryDropField);
