<template>
  <div class="bg-white rounded shadow-md ">

    <div class="editor">
      <!--  Menu bar   -->
      <editor-menu-bar :editor="editor" v-slot="{ commands, isActive, focused }">

        <div class="d-flex menubar flex-wrap"
             :class="{'hide-menu': !focused, 'show-menu': focused}">

          <button class="btn btn-light" :class="{ 'is-active': isActive.bold() }"
                  @click="commands.bold">
            <font-awesome-icon icon="bold"/>
          </button>

          <button class="btn btn-light" :class="{ 'is-active': isActive.italic() }"
                  @click="commands.italic">
            <font-awesome-icon icon="italic"/>
          </button>

          <button class="btn btn-light" :class="{ 'is-active': isActive.underline() }"
                  @click="commands.underline">
            <font-awesome-icon icon="underline"/>
          </button>

          <button class="btn btn-light" :class="{ 'is-active': isActive.strike() }"
                  @click="commands.strike">
            <font-awesome-icon icon="strikethrough"/>
          </button>

          <button class="btn btn-light" :class="{ 'is-active': isActive.heading({ level: 1 }) }"
                  @click="commands.heading({ level: 1 })">
            H1
          </button>

          <button class="btn btn-light" :class="{ 'is-active': isActive.heading({ level: 2 }) }"
                  @click="commands.heading({ level: 2 })">
            H2
          </button>

          <button class="btn btn-light" :class="{ 'is-active': isActive.heading({ level: 3 }) }"
                  @click="commands.heading({ level: 3 })">
            H3
          </button>

          <!-- <button class="btn btn-light" @click="showImagePrompt(commands.image)">
            <font-awesome-icon icon="image"/>
          </button> -->

          <button class="btn btn-light" :class="{ 'is-active': isActive.code() }"
                  @click="commands.code">
            <font-awesome-icon icon="code"/>
          </button>

          <button class="btn btn-light" :class="{ 'is-active': isActive.blockquote() }"
                  @click="commands.blockquote">
            <font-awesome-icon icon="quote-left"/>
          </button>

          <button class="btn btn-light" :class="{ 'is-active': isActive.bullet_list() }"
                  @click="commands.bullet_list">
            <font-awesome-icon icon="list-ul"/>
          </button>

          <button class="btn btn-light" :class="{ 'is-active': isActive.ordered_list() }"
                  @click="commands.ordered_list">
            <font-awesome-icon icon="list-ol"/>
          </button>

          <button class="btn btn-light" @click="commands.horizontal_rule">
            <font-awesome-icon icon="ruler-horizontal"/>
          </button>

          <button class="btn btn-light" @click="commands.undo">
            <font-awesome-icon icon="undo"/>
          </button>

          <button class="btn btn-light" @click="commands.redo">
            <font-awesome-icon icon="redo"/>
          </button>
        </div>
      </editor-menu-bar>
      <!--   Content Editor   -->
      <editor-content class="p-3 pl-0 text-left border border-dark" :editor="editor"/>
    </div>

    <!--  Custom buttons  -->
    <slot name="footer"></slot>

  </div>
</template>

<script>
import { Editor, EditorContent, EditorMenuBar } from 'tiptap'
import {
  Blockquote,
  Bold,
  BulletList,
  Code,
  Heading,
  History,
  HorizontalRule,
  Image,
  Italic,
  ListItem,
  OrderedList,
  Placeholder,
  Strike,
  Underline
} from 'tiptap-extensions'
import { library } from '@fortawesome/fontawesome-svg-core'
import {
  faBold,
  faCode,
  faImage,
  faItalic,
  faListOl,
  faListUl,
  faQuoteLeft,
  faRedo,
  faRulerHorizontal,
  faStrikethrough,
  faUnderline,
  faUndo
} from '@fortawesome/free-solid-svg-icons'
import Swal from 'sweetalert2'

library.add(faBold, faItalic, faQuoteLeft, faRulerHorizontal, faListUl,
  faListOl, faCode, faUndo, faRedo, faImage, faUnderline, faStrikethrough)

export default {
  components: {
    EditorContent,
    EditorMenuBar,
  },

  props: ["initialContent","placeholder"],

  data () {
    return {
      editor: new Editor({
        extensions: [new Blockquote(), new BulletList(), new HorizontalRule(), new Image(),
          new ListItem(), new Heading({ levels: [1, 2, 3] }), new OrderedList(),
          new Bold(), new Code(), new Italic(), new Strike(), new Underline(), new History(),
          new Placeholder({
            emptyEditorClass: 'is-editor-empty',
            emptyNodeClass: 'is-empty',
            emptyNodeText: this.placeholder,
            showOnlyWhenEditable: true,
            showOnlyCurrent: true,
          }),
        ],
        content: this.initialContent,
      }),
    }
  },

  methods: {
    showImagePrompt (command) {
        Swal.fire({
        title: 'Enter the url of your image',
        input: 'text',
        inputAttributes: { autocapitalize: 'off' },
        showCancelButton: true,
        confirmButtonText: 'Insert',
        showLoaderOnConfirm: true,
      }).then((result) => {
        const value = result.value
        if (value !== null) {
          command({ src: value })
        }
      })
    },
  },

  beforeDestroy () {
    this.editor.destroy()
  },

}
</script>

<style>
.ProseMirror-focused {
  outline: none;
}

.menubar.hide-menu {
    
  max-height:0px;
  opacity:0;
  transition-property: opacity, max-height;
  transition-duration: 0.25s;
  transition-timing-function: ease-out;
  transition-delay: 0s, 0.25s;
}

.menubar.show-menu {
  opacity:1;
  max-height:1000px;
  transition-property: opacity, max-height;
  transition-duration: 0.25s;
  transition-timing-function: ease-out;
  transition-delay: 0.25s, 0s;
}


.editor p.is-editor-empty:first-child::before {
  content: attr(data-empty-text);
  float: left;
  color: #aaa;
  pointer-events: none;
  height: 0;
  font-style: italic;
}
</style>
