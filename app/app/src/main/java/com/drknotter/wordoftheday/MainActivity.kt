package com.drknotter.wordoftheday

import android.os.Bundle
import android.util.Log
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.KeyboardArrowLeft
import androidx.compose.material.icons.filled.KeyboardArrowRight
import androidx.compose.material3.Button
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.Dialog
import com.drknotter.wordoftheday.ui.theme.Typography
import com.drknotter.wordoftheday.ui.theme.WordOfTheDayTheme
import java.time.DayOfWeek
import java.time.LocalDate
import java.time.format.DateTimeFormatter
import java.time.format.TextStyle
import java.time.temporal.ChronoUnit
import java.util.Locale

class MainActivity : ComponentActivity() {
  private lateinit var words: Map<Int, List<String>>

  private var currentMonthDay = mutableStateOf(LocalDate.now().withDayOfMonth(1))

  override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    words = buildMap {
      put(2022, resources.getStringArray(R.array.words_2022).asList())
      put(2023, resources.getStringArray(R.array.words_2023).asList())
      put(2024, resources.getStringArray(R.array.words_2024).asList())
    }
    setContent {
      var selectedDate: LocalDate? by remember { mutableStateOf(null) }
      WordOfTheDayTheme {
        // A surface container using the 'background' color from the theme
        Surface(
          modifier = Modifier.fillMaxSize(), color = MaterialTheme.colorScheme.background
        ) {
          Column {
            MonthHeader(
              dayInMonth = currentMonthDay.value,
              onThisMonth = { currentMonthDay.value = LocalDate.now().withDayOfMonth(1) },
              onPreviousMonth = { currentMonthDay.value = currentMonthDay.value.minusMonths(1) },
              onNextMonth = { currentMonthDay.value = currentMonthDay.value.plusMonths(1) }
            )
            Month(dayInMonth = currentMonthDay.value, onDaySelected = { selectedDate = it })
            selectedDate?.let {
              WordDialog(
                word = words[it.year]?.get(it.dayOfYear - 1) ?: "Missing word!",
                date = it,
                onDismissRequest = { selectedDate = null }
              )
            }
          }
        }
      }
    }
  }

  override fun onResume() {
    super.onResume()
    currentMonthDay.value = LocalDate.now().withDayOfMonth(1)
  }
}


fun daysOfMonth(date: LocalDate): List<LocalDate?> {
  val firstDayOfMonth: LocalDate = date.withDayOfMonth(1)
  val dayOfFirstDay: Int = firstDayOfMonth.dayOfWeek.value % 7
  return List(dayOfFirstDay) { null } + generateSequence(firstDayOfMonth) { it.plusDays(1) }.takeWhile { it.month == date.month }
    .toList()
}

@Composable
fun Day(date: LocalDate?, onDaySelected: (LocalDate) -> Unit) {
  Box(
    modifier = Modifier
      .aspectRatio(1f)
      .clickable { if (date != null) onDaySelected(date) },
    contentAlignment = Alignment.Center,
  ) {
    Box(
      modifier = Modifier
        .background(
          if (date?.equals(LocalDate.now()) == true) MaterialTheme.colorScheme.primary else Color.Transparent,
          shape = CircleShape
        )
        .border(
          width = if (date?.equals(LocalDate.now()) == true) 1.dp else 0.dp,
          color = if (date != null) MaterialTheme.colorScheme.primary else Color.Transparent,
          shape = CircleShape
        )
        .padding(4.dp)
    ) {
      Text(
        text = date?.format(DateTimeFormatter.ofPattern("d")) ?: "",
        modifier = Modifier.size(24.dp),
        textAlign = TextAlign.Center,
        style = Typography.bodyLarge,
        color = if (date?.equals(LocalDate.now()) == true) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onBackground
      )
    }
  }
}

@Composable
fun MonthHeader(dayInMonth: LocalDate, onThisMonth: () -> Unit, onPreviousMonth: () -> Unit, onNextMonth: () -> Unit) {
  val today = LocalDate.now();
  Column(Modifier.padding(16.dp)) {
    Row {
      Text(
        text = dayInMonth.format(DateTimeFormatter.ofPattern("MMMM yyyy")),
        modifier = Modifier
          .weight(1f)
          .align(Alignment.CenterVertically),
        style = MaterialTheme.typography.titleLarge
      )
      if (dayInMonth.year != today.year || dayInMonth.month != today.month) {
        Button(onClick = onThisMonth) {
          Text(text = "Today")
        }
      }
      IconButton(onClick = onPreviousMonth) {
        Icon(
          imageVector = Icons.Filled.KeyboardArrowLeft, contentDescription = "Previous"
        )
      }
      IconButton(onClick = onNextMonth) {
        Icon(
          imageVector = Icons.Filled.KeyboardArrowRight, contentDescription = "Next"
        )
      }
    }
  }
}

@Composable
fun Month(dayInMonth: LocalDate, onDaySelected: (LocalDate) -> Unit) {
  LazyVerticalGrid(columns = GridCells.Fixed(7)) {
    items(7) {
      Text(
        text = DayOfWeek.of(if (it == 0) 7 else it).getDisplayName(TextStyle.NARROW, Locale.US),
        textAlign = TextAlign.Center
      )
    }
    items(items = daysOfMonth(dayInMonth)) { day ->
      Day(day, onDaySelected)
    }
  }
}

@Composable
fun WordDialog(word: String, date: LocalDate, onDismissRequest: () -> Unit) {
  Dialog(onDismissRequest = { onDismissRequest() }) {
    Box(
      modifier = Modifier
        .fillMaxWidth()
        .height(200.dp)
        .padding(16.dp)
        .background(MaterialTheme.colorScheme.background, shape = RoundedCornerShape(16.dp)),
    ) {
      Column(modifier = Modifier.align(Alignment.Center),
        horizontalAlignment = Alignment.CenterHorizontally) {
        Text(
          text = "Day " + ChronoUnit.DAYS.between(
            LocalDate.of(2021, 12, 31),
            date
          ),
        )
        Text(
          text = word.uppercase(),
          style = MaterialTheme.typography.titleLarge,
          fontWeight = FontWeight.ExtraBold,
        )
      }
    }
  }
}

@Preview(showBackground = true, showSystemUi = true)
@Composable
fun WordOfTheDayPreview() {
  WordOfTheDayTheme {
    Month(dayInMonth = LocalDate.now()) { day -> Log.d("Preview", day.toString()) }
  }
}