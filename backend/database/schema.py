create_tables_query = {
    "CREATE_USERS_TABLE"           : "create table if not exists Users "
                                     "(uid text, name text, desc text default '', "
                                     "primary key (uid))",
    "CREATE_CONSULTING_TABLE"      : "create table if not exists Consulting "
                                     "(uid text, reg_date integer default 0, mod_date integer default 0, "
                                     "author text, "
                                     "subject text, "
                                     "body text, "
                                     "clicked integer, "
                                     "primary key (uid))",
    "CREATE_CONSULTING_REPLY_TABLE": "create table if not exists ConsultingReply "
                                     "(uid text, reg_date integer default 0, mod_date integer default 0, "
                                     "consulting_uid text, "
                                     "author text, "
                                     "body, "
                                     "primary key (uid))"
}
