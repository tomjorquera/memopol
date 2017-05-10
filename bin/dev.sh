#!/bin/bash
# Script to setup few usual aliases to facilitate the development
# This aliases should work if you've installed memopol throught the quickstart
# script or the documentation
# It :
#   - Setup automaticaly the venv
#   - Setup Django in DEBUG mode
# You just need to add a line in you're .bashrc or .zshrc to load them:

REPOROOT="$( readlink -m "${BASH_SOURCE[0]}"/../..)"
ALIASROOT=$REPOROOT"/.memopol.alias"
echo $ALIASROOT
echo "Create a dedicated alias file in $ALIASROOT"
echo "alias memopol-code=\"cd $REPOROOT && source $REPOROOT/memopol_env/bin/activate && DJANGO_DEBUG=True\"" > $ALIASROOT
echo "alias memopol-launch=\"memopol-code && memopol runserver\"" >> $ALIASROOT
echo "alias memopol-update-all=\"memopol-code && bin/update-all\"" >> $ALIASROOT
echo "alias memopol-refresh-scores=\"memopol-code && memopol refresh_scores\"" >> $ALIASROOT

case $SHELL in
*/bash)
	echo "Bash detected"
	echo "Update $HOME/.bashrc file"
	RCSHELL="$HOME/.bashrc"
	;;
*/zsh)
	echo "Zsh detected"
	echo "Update $HOME/.zshrc file"
	RCSHELL="$HOME/.zshrc"
	;;
*)
	echo "SHELL don't supported.  Try using BASH or ZSH, or manually."
	;;
esac

echo "source $ALIASROOT" >> $RCSHELL
source $ALIASROOT


echo -e "You can use the following aliases :\n"
echo -e "\t memopol-code : Go into the repository and activate the virtualenv"
echo -e "\t memopol-launch : Run the development server"
echo -e "\t memopoll-update-all : Get all the production data"
echo -e "\t memopol-refresh-scores : Refresh all scores"
