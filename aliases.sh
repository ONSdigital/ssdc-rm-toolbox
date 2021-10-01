shopt -s expand_aliases
alias findpubsubmessages='python -m toolbox.message_tools.get_pubsub_messages'
alias pubsubmessagetobucket='python -m toolbox.message_tools.put_message_on_bucket'
alias buckettopubsub='python -m toolbox.message_tools.publish_message_from_bucket'
alias dosql='dosql.sh'
alias dosql-i-know-what-i-am-doing='i_know_what_i_am_doing.sh n00dleBla5terBadg3r'
alias helpme='echo "Commands: helpme, msgwizard, vi, curl, dosql [username], sftp, dumpfilestoqueue, dumpqueuetofiles, qidcheck [qid]"'
alias downloadfilefrombucket='python -m toolbox.download_file_from_bucket'
alias uploadfiletobucket='python -m toolbox.upload_file_to_bucket'
alias msgwizard='python -m toolbox.message_tools.bad_message_wizard'
alias qidcheck='python -m toolbox.qid_checksum_validator --modulus $QID_MODULUS --factor $QID_FACTOR'
alias doftp='sftp -i $SFTP_KEY_FILENAME $SFTP_USERNAME@$SFTP_HOST'
alias dumpsubscriptiontofiles='python -m toolbox.message_tools.dump_subscription_to_files'
alias dumpfilestotopic='python -m toolbox.message_tools.dump_files_to_topic'
alias validatesample='python -m toolbox.sample_loader.validate_sample'
alias loadsample='python -m toolbox.sample_loader.load_sample'
