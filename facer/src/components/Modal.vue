<template>
    <div>
        <transition name="mymodal">
            <div v-if="isOpen">
                <div class="overlay" @click.self="setclose()">
                    <div class="mymodal" @click.self="setclose()">
                        <h1>에러</h1>
                        <p>빈칸을 모두 채워주셔야 합니다</p>
                    </div>
                </div>
            </div>
        </transition>
    </div>
</template>

<script>
    import {mapGetters} from 'vuex';

    export default {
        name: "Modal",
        computed: {
            ...mapGetters({
                isOpen: 'modal/isOpen'
            })
        },
        methods:{
            setclose(){
                this.$store.commit('modal/setClose');
            },
        }
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