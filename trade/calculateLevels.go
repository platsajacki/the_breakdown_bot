package main

import (
	"encoding/json"
	"io"
	"os"
)

const (
	count_match = 2
)

// findLevelMatch looks for matches in prices.
// If the price level matches more than 2, we consider it a level.
func findLevelMatch(prices []string) map[string]int {
	levels := make(map[string]int)
	for _, currentPrice := range prices {
		count := 0
		for _, price := range prices {
			if currentPrice == price {
				count++
			}
		}
		if count > count_match {
			levels[currentPrice] = count
		}
	}
	return levels
}

// mergeLevels merges two maps of price levels.
func mergeLevels(lowLevels map[string]int, highLevels map[string]int) map[string]int {
	for key, lowValue := range lowLevels {
		highValue, exists := highLevels[key]
		if exists {
			highLevels[key] = lowValue + highValue
		} else {
			highLevels[key] = lowValue
		}
	}
	return highLevels
}

// findLevelIntersection finds intersections
// between two sets of price levels and updates the levels map.
func findLevelIntersection(lowPrices []string, highPrices []string, levels map[string]int) map[string]int {
	for _, currentPrice := range lowPrices {
		count := 0
		for _, price := range highPrices {
			if currentPrice == price {
				count++
			}
		}
		if count > count_match {
			value, exists := levels[currentPrice]
			if exists {
				levels[currentPrice] = count + value
			} else {
				levels[currentPrice] = count
			}
		}
	}
	return levels
}

// getCoinLevels calculates price levels for a given symbol's data.
func getCoinLevels(symbol_data [][7]string) map[string]int {
	var lowPrices []string
	var highPrice []string
	for _, day := range symbol_data {
		lowPrices = append(lowPrices, day[2])
		highPrice = append(highPrice, day[3])
	}
	levels := mergeLevels(findLevelMatch(lowPrices), findLevelMatch(highPrice))
	return findLevelIntersection(lowPrices, highPrice, levels)
}

func main() {
	jsonData, readError := io.ReadAll(os.Stdin)
	if readError != nil {
		panic(readError)
	}
	var symbolsData map[string][][7]string
	unmarshalError := json.Unmarshal(jsonData, &symbolsData)
	if unmarshalError != nil {
		panic(unmarshalError)
	}
	result := make(map[string]map[string]int)
	for symbol, data := range symbolsData {
		result[symbol] = getCoinLevels(data)
	}
	jsonResult, marshalError := json.Marshal(result)
	if marshalError != nil {
		panic(marshalError)
	}
	os.Stdout.Write(jsonResult)
}
