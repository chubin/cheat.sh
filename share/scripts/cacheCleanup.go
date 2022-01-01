package main

// Remove invalid cache entries.
// Cache entry is invalid, if it contains a special substring.

import (
	"context"
	"log"
	"strings"

	"github.com/go-redis/redis"
)

var invalidEntrySubstr = "Unknown cheat sheet"

func removeInvalidEntries() error {
	rdb := redis.NewClient(&redis.Options{
		Addr:     "localhost:6379",
		Password: "",
		DB:       0,
	})

	ctx := context.Background()
	allKeys, err := rdb.Keys(ctx, "*").Result()
	if err != nil {
		return err
	}

	var counter int
	for _, key := range allKeys {
		val, err := rdb.Get(ctx, key).Result()
		if err != nil {
			return err
		}
		if strings.Contains(val, invalidEntrySubstr) {
			err = rdb.Del(ctx, key).Err()
			if err != nil {
				return err
			}
			counter++
		}
	}
	log.Println("invalid entries removed:", counter)
	return nil
}

func main() {
	err := removeInvalidEntries()
	if err != nil {
		log.Println(err)
	}
}
