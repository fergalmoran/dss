SELECT spa__activity.`date`, spa__activity.user_id, spa_mixplay.mix_id
  FROM    deepsouthsounds.spa_mixplay spa_mixplay
       INNER JOIN
          deepsouthsounds.spa__activity spa__activity
       ON (spa_mixplay._activity_ptr_id = spa__activity.id)