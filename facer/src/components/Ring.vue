<template>
    <div v-if="ringState">
        <transition name="mymodal">
            <div>
                <div class="overlay">
                    <div class="mymodal">
                        <DashedSpinner>얼굴 분석 중입니다</DashedSpinner>
                    </div>
                </div>
            </div>
        </transition>
    </div>
</template>

<script>
    import {mapGetters} from "vuex"

    export default {
        name: "Ring",
        computed: {
            ...mapGetters({
                ringState: 'ring/ringState',
            })
        },
    }
</script>

<style scoped>
    .mymodal {
        width: 500px;
        margin: 0px auto;
        padding: 20px;
        background-color: #fff;
        border-radius: 2px;
        box-shadow: 0 2px 8px 3px;
        transition: all 0.2s ease-in;
        font-family: Helvetica, Arial, sans-serif;
    }
    .fadeIn-enter {
        opacity: 0;
    }

    .fadeIn-leave-active {
        opacity: 0;
        transition: all 0.2s step-end;
    }

    .fadeIn-enter .mymodal,
    .fadeIn-leave-active.modal {
        transform: scale(1.1);
    }

    .overlay {
        position: fixed;
        top: 0;
        left: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        height: 100%;
        background: #00000094;
        z-index: 999;
        transition: opacity 0.2s ease;
    }
</style>