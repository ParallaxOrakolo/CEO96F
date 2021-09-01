import { mapState } from "vuex";

export default {
    computed: {
        ...mapState(["configuration"]),
    },

    methods: {

        isUserAcessPermited(componentName) {
            let userLogged = this.configuration.informations.users.logged
            let levelList = this.configuration.informations.users.levelList
            let isPermited = false
            let selectedLevel = null
            let isEqual = false

            function Equal(item) {
                if (item == componentName) {
                    isEqual = true
                }
            }

            function findLevel(item) {
                if (item.name == userLogged.level) {
                    selectedLevel = item
                }
            }

            if (userLogged) {
                levelList.forEach(findLevel)
                selectedLevel.componentsProhibitedAccess.forEach(Equal)

                if (isEqual) {
                    isPermited = false
                }else{
                    isPermited = true
                }

                return isPermited
            }
        }
    }
}