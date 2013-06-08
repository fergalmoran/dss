SELECT spa__activity.`date`, spa__activity.user_id, spa_mixdownload.mix_id
  FROM    deepsouthsounds.spa_mixdownload spa_mixdownload
       INNER JOIN
          deepsouthsounds.spa__activity spa__activity
       ON (spa_mixdownload._activity_ptr_id = spa__activity.id)